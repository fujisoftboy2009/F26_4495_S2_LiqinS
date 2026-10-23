from flask import Flask, render_template
import joblib
import os

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


@app.route("/")
def home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)