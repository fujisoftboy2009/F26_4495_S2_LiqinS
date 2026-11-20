from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
import joblib
import os
import webbrowser
from threading import Timer

app = Flask(__name__)

app.secret_key = os.environ.get(
    "SECRET_KEY",
    "development-secret-key"
)

# Get the current webapp folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Get the models folder
MODELS_DIR = os.path.join(BASE_DIR, "..", "models")

# Load saved preprocessing pipeline and model
preprocessor = joblib.load(
    os.path.join(MODELS_DIR, "preprocessor.pkl"))

model = joblib.load(
    os.path.join(MODELS_DIR, "weighted_logistic_model.pkl"))

@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        session["step1"] = {
            "Age": request.form["Age"],
            "Sex": request.form["Sex"],
            "Race_Ethnicity": request.form["Race_Ethnicity"],
            "Education": request.form["Education"],
            "Income_Group": request.form["Income_Group"]
        }

        return redirect(url_for("health_information"))

    return render_template("index.html")



@app.route("/health-information", methods=["GET", "POST"])
def health_information():

    if request.method == "POST":

        session["step2"] = {
            "BMI": request.form["BMI"],
            "HighBP": request.form["HighBP"],
            "HighChol": request.form["HighChol"],
            "General_Health": request.form["General_Health"]
        }

        return redirect(url_for("lifestyle"))

    return render_template("healthInformation.html")

@app.route("/lifestyle", methods=["GET", "POST"])
def lifestyle():

    if request.method == "POST":

        session["step3"] = {
            "Smoking_Status": request.form["Smoking_Status"],
            "Physical_Activity": request.form["Physical_Activity"],
            "Fruit_Per_Day": request.form["Fruit_Per_Day"],
            "Vegetable_Per_Day": request.form["Vegetable_Per_Day"]
        }

        return redirect(url_for("review"))

    return render_template("lifestyle.html")

def open_browser():
    webbrowser.open("http://127.0.0.1:5000")

if __name__ == "__main__":

    # Open the web page automatically
    if os.environ.get("WERKZEUG_RUN_MAIN") != "true":
        Timer(1, open_browser).start()

    app.run(debug=True)