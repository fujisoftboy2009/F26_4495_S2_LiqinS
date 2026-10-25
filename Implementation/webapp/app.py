from flask import Flask, render_template, request
import pandas as pd
import joblib
import os
import webbrowser
from threading import Timer

app = Flask(__name__)

# Get the current webapp folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Get the models folder
MODELS_DIR = os.path.join(BASE_DIR, "..", "models")

# Load saved preprocessing pipeline and model
preprocessor = joblib.load(
    os.path.join(MODELS_DIR, "preprocessor.pkl")
)

model = joblib.load(
    os.path.join(MODELS_DIR, "weighted_logistic_model.pkl")
)


@app.route("/", methods=["GET", "POST"])
def home():

    prediction = None
    probabilities = None

    if request.method == "POST":

        # Get the 13 inputs from the web form
        new_person = pd.DataFrame([{
            "Age": float(request.form["Age"]),
            "Sex": request.form["Sex"],
            "BMI": float(request.form["BMI"]),
            "HighBP": request.form["HighBP"],
            "Smoking_Status": request.form["Smoking_Status"],
            "HighChol": request.form["HighChol"],
            "Physical_Activity": request.form["Physical_Activity"],
            "Education": request.form["Education"],
            "Income_Group": request.form["Income_Group"],
            "Race_Ethnicity": request.form["Race_Ethnicity"],
            "Fruit_Per_Day": float(request.form["Fruit_Per_Day"]),
            "Vegetable_Per_Day": float(request.form["Vegetable_Per_Day"]),
            "General_Health": request.form["General_Health"]
        }])

        # Process the input using the saved preprocessing pipeline
        processed_input = preprocessor.transform(new_person)

        # Make prediction
        prediction = model.predict(processed_input)[0]

        # Get prediction scores
        probabilities = dict(
            zip(model.classes_, model.predict_proba(processed_input)[0]
                )
)

        print("Prediction:", prediction)
        print("Classes:", model.classes_)
        print("Prediction scores:", probabilities)

    return render_template(
        "index.html",    
        prediction=prediction,
        probabilities=probabilities)


def open_browser():
    webbrowser.open("http://127.0.0.1:5000")


if __name__ == "__main__":

    # Open the web page automatically
    if os.environ.get("WERKZEUG_RUN_MAIN") != "true":
        Timer(1, open_browser).start()

    app.run(debug=True)