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

    return render_template(
        "index.html",
        form_data=session.get("step1", {})
    )


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


@app.route("/review", methods=["GET", "POST"])
def review():

    step1 = session.get("step1")
    step2 = session.get("step2")
    step3 = session.get("step3")

    if not step1 or not step2 or not step3:
        return redirect(url_for("home"))

    answers = {
        **step1,
        **step2,
        **step3
    }

    # User clicks Predict Risk
    if request.method == "POST":

        new_person = pd.DataFrame([{
            "Age": float(answers["Age"]),
            "Sex": answers["Sex"],
            "BMI": float(answers["BMI"]),
            "HighBP": answers["HighBP"],
            "Smoking_Status": answers["Smoking_Status"],
            "HighChol": answers["HighChol"],
            "Physical_Activity": answers["Physical_Activity"],
            "Education": answers["Education"],
            "Income_Group": answers["Income_Group"],
            "Race_Ethnicity": answers["Race_Ethnicity"],
            "Fruit_Per_Day": float(answers["Fruit_Per_Day"]),
            "Vegetable_Per_Day": float(answers["Vegetable_Per_Day"]),
            "General_Health": answers["General_Health"]
        }])

        processed_input = preprocessor.transform(new_person)

        prediction = model.predict(processed_input)[0]

        probabilities = dict(
            zip(
                model.classes_,
                model.predict_proba(processed_input)[0]
            )
        )

        return render_template(
            "result.html",
            prediction=prediction,
            probabilities=probabilities
        )

    return render_template(
        "review.html",
        answers=answers
    )

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/about")
def about():
    return render_template("about.html")

def open_browser():
    webbrowser.open("http://127.0.0.1:5000")

if __name__ == "__main__":

    # Open browser only once when running locally
    if os.environ.get("WERKZEUG_RUN_MAIN") != "true":
        Timer(1, open_browser).start()

    app.run(debug=True)