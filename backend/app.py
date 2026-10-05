from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
import os
import sqlite3
import secrets

from werkzeug.security import generate_password_hash, check_password_hash


# =========================================================
# APP CONFIGURATION
# =========================================================

app = Flask(__name__)

CORS(app)

BASE_DIR = os.path.dirname(__file__)

DATABASE_DIR = os.path.join(BASE_DIR, "database")
DATABASE_PATH = os.path.join(DATABASE_DIR, "scrapsetu.db")

MODEL_PATH = os.path.join(
    BASE_DIR,
    "model",
    "model.pkl"
)


# Create database folder if it doesn't exist
os.makedirs(DATABASE_DIR, exist_ok=True)


# =========================================================
# LOAD ML MODEL
# =========================================================

model = joblib.load(MODEL_PATH)

print("ML model loaded successfully!")


# =========================================================
# DATABASE CONNECTION
# =========================================================

def get_db():

    connection = sqlite3.connect(DATABASE_PATH)

    connection.row_factory = sqlite3.Row

    return connection


# =========================================================
# INITIALIZE DATABASE
# =========================================================

def init_db():

    db = get_db()

    cursor = db.cursor()

    # -------------------------
    # USERS
    # -------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT NOT NULL,

            email TEXT UNIQUE NOT NULL,

            password TEXT NOT NULL,

            role TEXT DEFAULT 'user',

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
    """)


    # -------------------------
    # SCRAP RATES
    # -------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scrap_rates (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            material TEXT UNIQUE NOT NULL,

            category TEXT,

            base_price REAL NOT NULL,

            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
    """)


    # -------------------------
    # PICKUPS
    # -------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pickups (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER NOT NULL,

            material TEXT NOT NULL,

            quality TEXT NOT NULL,

            weight REAL NOT NULL,

            estimated_price REAL NOT NULL,

            address TEXT NOT NULL,

            city TEXT NOT NULL,

            pickup_date TEXT NOT NULL,

            pickup_time TEXT NOT NULL,

            status TEXT DEFAULT 'Pending',

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(user_id) REFERENCES users(id)

        )
    """)


    # -------------------------
    # CONTACT MESSAGES
    # -------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contacts (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT NOT NULL,

            email TEXT NOT NULL,

            subject TEXT NOT NULL,

            message TEXT NOT NULL,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
    """)


    # -------------------------
    # DEFAULT SCRAP RATES
    # -------------------------

    default_rates = [

        ("Copper", "Metal", 500),
        ("Iron", "Metal", 35),
        ("Aluminium", "Metal", 150),
        ("Brass", "Metal", 400),
        ("Plastic", "Recyclable", 30),
        ("Paper", "Recyclable", 15)

    ]


    for material, category, price in default_rates:

        cursor.execute("""
            INSERT OR IGNORE INTO scrap_rates
            (material, category, base_price)

            VALUES (?, ?, ?)
        """, (material, category, price))


    db.commit()

    db.close()


# Initialize database
init_db()


# =========================================================
# SIMPLE TOKEN STORAGE
# =========================================================

# Development version.
# Later we can replace this with JWT authentication.

active_tokens = {}


# =========================================================
# HOME ROUTE
# =========================================================

@app.route("/")
def home():

    return jsonify({

        "success": True,

        "message": "ScrapSetu Backend API is running!",

        "services": [

            "ML Price Prediction",
            "User Authentication",
            "Scrap Rates",
            "Pickup Booking",
            "Contact"

        ]

    })


# =========================================================
# ML PRICE PREDICTION
# =========================================================

@app.route("/predict", methods=["POST"])
def predict():

    try:

        data = request.get_json()

        # -------------------------
        # GET INPUT
        # -------------------------

        state = data["state"]

        city = data["city"]

        material = data["material"]

        quality = data["quality"]

        weight = float(data["weight"])

        date = data["date"]


        # -------------------------
        # VALIDATION
        # -------------------------

        if weight <= 0:

            return jsonify({

                "success": False,

                "error": "Weight must be greater than 0."

            }), 400


        # -------------------------
        # DATE
        # -------------------------

        date_obj = pd.to_datetime(date)

        year = date_obj.year

        month = date_obj.month

        day = date_obj.day


        # -------------------------
        # MODEL INPUT
        # -------------------------

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


        # -------------------------
        # ML PREDICTION
        # -------------------------

        predicted_price = model.predict(input_data)[0]


        # -------------------------
        # TOTAL VALUE
        # -------------------------

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


# =========================================================
# REGISTER
# =========================================================

@app.route("/api/register", methods=["POST"])
def register():

    try:

        data = request.get_json()

        name = data.get("name", "").strip()

        email = data.get("email", "").strip().lower()

        password = data.get("password", "")


        # Validation

        if not name:

            return jsonify({

                "success": False,

                "error": "Name is required."

            }), 400


        if not email:

            return jsonify({

                "success": False,

                "error": "Email is required."

            }), 400


        if len(password) < 6:

            return jsonify({

                "success": False,

                "error": "Password must contain at least 6 characters."

            }), 400


        db = get_db()

        cursor = db.cursor()


        # Check existing email

        existing_user = cursor.execute(
            "SELECT id FROM users WHERE email = ?",
            (email,)
        ).fetchone()


        if existing_user:

            db.close()

            return jsonify({

                "success": False,

                "error": "Email already registered."

            }), 409


        # Hash password

        hashed_password = generate_password_hash(password)


        cursor.execute("""
            INSERT INTO users
            (name, email, password)

            VALUES (?, ?, ?)
        """, (

            name,

            email,

            hashed_password

        ))


        db.commit()

        user_id = cursor.lastrowid

        db.close()


        return jsonify({

            "success": True,

            "message": "Account created successfully.",

            "user": {

                "id": user_id,

                "name": name,

                "email": email

            }

        }), 201


    except Exception as e:

        return jsonify({

            "success": False,

            "error": str(e)

        }), 500


# =========================================================
# LOGIN
# =========================================================

@app.route("/api/login", methods=["POST"])
def login():

    try:

        data = request.get_json()

        email = data.get("email", "").strip().lower()

        password = data.get("password", "")


        db = get_db()

        user = db.execute(
            "SELECT * FROM users WHERE email = ?",
            (email,)
        ).fetchone()

        db.close()


        if not user:

            return jsonify({

                "success": False,

                "error": "Invalid email or password."

            }), 401


        if not check_password_hash(
            user["password"],
            password
        ):

            return jsonify({

                "success": False,

                "error": "Invalid email or password."

            }), 401


        # Generate login token

        token = secrets.token_hex(32)

        active_tokens[token] = user["id"]


        return jsonify({

            "success": True,

            "message": "Login successful.",

            "token": token,

            "user": {

                "id": user["id"],

                "name": user["name"],

                "email": user["email"],

                "role": user["role"]

            }

        })


    except Exception as e:

        return jsonify({

            "success": False,

            "error": str(e)

        }), 500


# =========================================================
# SCRAP RATES
# =========================================================

@app.route("/api/rates", methods=["GET"])
def get_rates():

    try:

        db = get_db()

        rates = db.execute(
            "SELECT * FROM scrap_rates ORDER BY material"
        ).fetchall()

        db.close()


        result = []

        for rate in rates:

            result.append({

                "id": rate["id"],

                "material": rate["material"],

                "category": rate["category"],

                "base_price": rate["base_price"]

            })


        return jsonify({

            "success": True,

            "rates": result

        })


    except Exception as e:

        return jsonify({

            "success": False,

            "error": str(e)

        }), 500


# =========================================================
# AUTHENTICATION HELPER
# =========================================================

def get_logged_in_user():

    auth_header = request.headers.get("Authorization")

    if not auth_header:

        return None


    if not auth_header.startswith("Bearer "):

        return None


    token = auth_header.split(" ")[1]

    user_id = active_tokens.get(token)


    if not user_id:

        return None


    db = get_db()

    user = db.execute(
        "SELECT * FROM users WHERE id = ?",
        (user_id,)
    ).fetchone()

    db.close()


    return user


# =========================================================
# CREATE PICKUP
# =========================================================

@app.route("/api/pickups", methods=["POST"])
def create_pickup():

    try:

        user = get_logged_in_user()


        if not user:

            return jsonify({

                "success": False,

                "error": "Please login first."

            }), 401


        data = request.get_json()


        material = data.get("material")

        quality = data.get("quality")

        weight = float(data.get("weight"))

        estimated_price = float(
            data.get("estimated_price")
        )

        address = data.get("address")

        city = data.get("city")

        pickup_date = data.get("pickup_date")

        pickup_time = data.get("pickup_time")


        if not all([

            material,

            quality,

            address,

            city,

            pickup_date,

            pickup_time

        ]):

            return jsonify({

                "success": False,

                "error": "All pickup fields are required."

            }), 400


        if weight <= 0:

            return jsonify({

                "success": False,

                "error": "Weight must be greater than 0."

            }), 400


        db = get_db()

        cursor = db.cursor()


        cursor.execute("""
            INSERT INTO pickups
            (
                user_id,
                material,
                quality,
                weight,
                estimated_price,
                address,
                city,
                pickup_date,
                pickup_time
            )

            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (

            user["id"],

            material,

            quality,

            weight,

            estimated_price,

            address,

            city,

            pickup_date,

            pickup_time

        ))


        db.commit()

        pickup_id = cursor.lastrowid

        db.close()


        return jsonify({

            "success": True,

            "message": "Pickup booked successfully.",

            "pickup_id": pickup_id,

            "status": "Pending"

        }), 201


    except Exception as e:

        return jsonify({

            "success": False,

            "error": str(e)

        }), 500


# =========================================================
# GET USER PICKUPS
# =========================================================

@app.route("/api/pickups", methods=["GET"])
def get_pickups():

    try:

        user = get_logged_in_user()


        if not user:

            return jsonify({

                "success": False,

                "error": "Please login first."

            }), 401


        db = get_db()


        pickups = db.execute("""
            SELECT *

            FROM pickups

            WHERE user_id = ?

            ORDER BY created_at DESC

        """, (user["id"],)).fetchall()


        db.close()


        result = []


        for pickup in pickups:

            result.append({

                "id": pickup["id"],

                "material": pickup["material"],

                "quality": pickup["quality"],

                "weight": pickup["weight"],

                "estimated_price": pickup["estimated_price"],

                "address": pickup["address"],

                "city": pickup["city"],

                "pickup_date": pickup["pickup_date"],

                "pickup_time": pickup["pickup_time"],

                "status": pickup["status"],

                "created_at": pickup["created_at"]

            })


        return jsonify({

            "success": True,

            "pickups": result

        })


    except Exception as e:

        return jsonify({

            "success": False,

            "error": str(e)

        }), 500


# =========================================================
# GET SINGLE PICKUP / TRACKING
# =========================================================

@app.route("/api/pickups/<int:pickup_id>", methods=["GET"])
def get_single_pickup(pickup_id):

    try:

        user = get_logged_in_user()


        if not user:

            return jsonify({

                "success": False,

                "error": "Please login first."

            }), 401


        db = get_db()


        pickup = db.execute("""
            SELECT *

            FROM pickups

            WHERE id = ?

            AND user_id = ?

        """, (

            pickup_id,

            user["id"]

        )).fetchone()


        db.close()


        if not pickup:

            return jsonify({

                "success": False,

                "error": "Pickup not found."

            }), 404


        return jsonify({

            "success": True,

            "pickup": {

                "id": pickup["id"],

                "material": pickup["material"],

                "quality": pickup["quality"],

                "weight": pickup["weight"],

                "estimated_price": pickup["estimated_price"],

                "address": pickup["address"],

                "city": pickup["city"],

                "pickup_date": pickup["pickup_date"],

                "pickup_time": pickup["pickup_time"],

                "status": pickup["status"]

            }

        })


    except Exception as e:

        return jsonify({

            "success": False,

            "error": str(e)

        }), 500


# =========================================================
# CONTACT
# =========================================================

@app.route("/api/contact", methods=["POST"])
def contact():

    try:

        data = request.get_json()


        name = data.get("name", "").strip()

        email = data.get("email", "").strip()

        subject = data.get("subject", "").strip()

        message = data.get("message", "").strip()


        if not all([

            name,

            email,

            subject,

            message

        ]):

            return jsonify({

                "success": False,

                "error": "All fields are required."

            }), 400


        db = get_db()


        db.execute("""
            INSERT INTO contacts
            (name, email, subject, message)

            VALUES (?, ?, ?, ?)
        """, (

            name,

            email,

            subject,

            message

        ))


        db.commit()

        db.close()


        return jsonify({

            "success": True,

            "message": "Message received successfully."

        }), 201


    except Exception as e:

        return jsonify({

            "success": False,

            "error": str(e)

        }), 500


# =========================================================
# RUN SERVER
# =========================================================

if __name__ == "__main__":

    app.run(

        debug=True,

        port=5000

    )