from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
import os


app = Flask(__name__)
CORS(app)


# --------------------------------
# Load trained ML model
# --------------------------------

model_path = os.path.join(
    os.path.dirname(__file__),
    "model",
    "model.pkl"
)

model = joblib.load(model_path)

print("ML model loaded successfully!")


# --------------------------------
# Home route
# --------------------------------

@app.route("/")
def home():
    return jsonify({
        "message": "Garbage Price Prediction API is running!"
    })


# --------------------------------
# Prediction API
# --------------------------------

@app.route("/predict", methods=["POST"])
def predict():

    try:

        data = request.get_json()

        # -----------------------------
        # Get input from frontend
        # -----------------------------

        state = data["state"]
        city = data["city"]
        material = data["material"]
        quality = data["quality"]
        weight = float(data["weight"])
        date = data["date"]


        # -----------------------------
        # Convert date
        # -----------------------------

        date_obj = pd.to_datetime(date)

        year = date_obj.year
        month = date_obj.month
        day = date_obj.day


        # -----------------------------
        # Create DataFrame
        # -----------------------------

        input_data = pd.DataFrame({
            "State": [state],
            "City": [city],
            "Material": [material],
            "Quality": [quality],
            "Weight": [weight],
            "Location": [city],
            "Year": [year],
            "Month": [month],
            "Day": [day]
        })


        # -----------------------------
        # Prediction
        # -----------------------------

        predicted_price = model.predict(input_data)[0]


        # -----------------------------
        # Calculate total value
        # -----------------------------

        total_price = predicted_price * weight


        return jsonify({
            "success": True,
            "price_per_kg": round(float(predicted_price), 2),
            "weight": weight,
            "total_price": round(float(total_price), 2)
        })


    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 400


# --------------------------------
# Run server
# --------------------------------

if __name__ == "__main__":
    app.run(debug=True, port=5000)