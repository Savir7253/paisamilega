# ♻️ Garbage Price Prediction

Garbage Price Prediction is a Machine Learning based web application that predicts the approximate scrap/waste price per kilogram based on different factors such as state, city, material, quality, and date.

The application also calculates the estimated total value based on the weight of the waste material.

---

## 🚀 Features

- ♻️ Predict scrap price per kg
- 📍 State and city based prediction
- 🧱 Supports multiple waste materials
- ⭐ Quality-based prediction
- 📅 Date-based price prediction
- ⚖️ Calculates estimated total value based on weight
- 🤖 Machine Learning powered prediction
- 🌐 Web-based frontend
- 🐍 Python Flask backend
- 🔗 Frontend and backend connected through REST API

---

## 🧱 Supported Materials

Currently, the application supports:

- Copper
- Iron
- Aluminium
- Brass
- Plastic
- Paper

### Quality Levels

- Good
- Medium
- Poor

---

## 🛠️ Technologies Used

### Frontend
- HTML
- CSS
- JavaScript

### Backend
- Python
- Flask
- Flask-CORS
- Pandas

### Machine Learning
- Scikit-learn
- Random Forest Regression
- One-Hot Encoding
- Joblib

### Dataset
- CSV
- 2520 records
- Multiple Indian states and cities
- Material, quality, weight and date-based data

---

## 🤖 Machine Learning Model

The project uses a **Random Forest Regression** model to predict the price per kilogram.

### Input Features

The model uses:

- State
- City
- Material
- Quality
- Weight
- Location
- Year
- Month
- Day

### Target

```text
Price_per_kg
