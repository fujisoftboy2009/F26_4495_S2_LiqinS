# Developing a Diabetes and Prediabetes Prediction Web App Using 2025 CDC BRFSS Data

## Project Description

This individual CSIS 4495 Applied Research project uses the 2025 CDC Behavioral Risk Factor Surveillance System (BRFSS) data to build a three-class machine learning model for:

- No Diabetes
- Prediabetes
- Diabetes

The project focuses on whether self-reported demographic, lifestyle, and health information can be used to classify reported diabetes status.

The final model is a **Weighted Logistic Regression** model. A simple Flask web application allows a user to enter 13 health-related inputs and receive a predicted class and prediction scores for all three classes.

This project is a research and educational demonstration only. It is **not a medical diagnostic tool** and does not replace blood testing or professional medical advice.

## Data Source

The project uses the **2025 CDC BRFSS public-use dataset**.

Original dataset size:

- 356,158 rows
- 283 columns

After removing records with missing target values, the modeling dataset contains 352,705 records.

Target class distribution:

- No Diabetes: 82.42%
- Diabetes: 14.69%
- Prediabetes: 2.88%

## Model Inputs

The final Model A uses 13 predictors:

1. Age
2. Sex
3. BMI
4. High Blood Pressure
5. Smoking Status
6. High Cholesterol
7. Physical Activity
8. Education
9. Income Group
10. Race / Ethnicity
11. Fruit Intake
12. Vegetable Intake
13. General Health

## Model Development

The following approaches were tested:

- Baseline Logistic Regression
- Baseline Random Forest
- Weighted Logistic Regression
- Weighted Random Forest
- Random Oversampling with Logistic Regression
- Random Oversampling with Random Forest
- Custom Class Weight Logistic Regression
- HistGradientBoosting
- Model B with additional healthcare access variables

**Weighted Logistic Regression** was selected because it provided the best overall balance for detecting Prediabetes while remaining simple and interpretable.

The selected model improved Prediabetes recall compared with the baseline models, although Prediabetes remained the most difficult class to predict.

## Web Application

The Flask application:

1. Accepts 13 inputs from the web form.
2. Creates a pandas DataFrame from the submitted values.
3. Applies the saved preprocessing pipeline.
4. Uses the saved Weighted Logistic Regression model.
5. Displays the predicted class.
6. Displays prediction scores for Diabetes, No Diabetes, and Prediabetes.

## Project Structure

```text
F26_4495_S2_LiqinS
├── DocumentsAndReports
├── Implementation
│   ├── DiabetesAnalysis.ipynb
│   ├── models
│   │   ├── preprocessor.pkl
│   │   └── weighted_logistic_model.pkl
│   └── webapp
│       ├── app.py
│       └── templates
│           └── index.html
└── README.md
```

## Installation Instructions

### 1. Download or clone the repository

Download the repository from GitHub or clone it to your computer.

### 2. Open a terminal in the `Implementation/webapp` folder

Example:

```text
F26_4495_S2_LiqinS/Implementation/webapp
```

### 3. Activate the Python environment

This project was tested using an Anaconda base environment.

```bash
conda activate base
```

### 4. Install required Python packages if needed

```bash
python -m pip install flask pandas joblib scikit-learn
```

### 5. Run the Flask application

```bash
python app.py
```

The local web page should open automatically in the default browser.

If it does not open automatically, go to:

```text
http://127.0.0.1:5000
```

### 6. Test the prediction

Enter values for all 13 fields and click **Predict**.

The page will display:

- Predicted class
- Diabetes prediction score
- No Diabetes prediction score
- Prediabetes prediction score

## Scenario Testing

Two hypothetical profiles were also compared with existing diabetes risk tools.

### Case 1: Lower-risk profile

- CDC Prediabetes Risk Test: 4/10, Low Risk
- Canadian CANRISK: 27, Moderate Risk
- BRFSS model: Prediabetes, 52.0% prediction score

### Case 2: Higher-risk profile

- CDC Prediabetes Risk Test: 9/10, High Risk
- Canadian CANRISK: 75, High Risk
- BRFSS model: Diabetes
  - Diabetes: 50.6%
  - Prediabetes: 45.7%
  - No Diabetes: 3.7%

These comparisons are only scenario-based reasonableness checks. The tools use different predictors and methods, so their results are not directly equivalent.

## Limitations

- BRFSS diabetes status is based on self-reported prior diagnosis.
- Some undiagnosed cases may be included in the No Diabetes group.
- Prediabetes is a small minority class and is difficult to separate from the other two classes.
- The prediction scores should not be interpreted as clinical probabilities.
- The application is for course demonstration and research purposes only.

## Current Project Status

Completed:

- Data cleaning and feature preparation
- Exploratory data analysis
- Train/test split and preprocessing
- Baseline model development
- Class imbalance testing
- Final model selection
- Saved preprocessing and model files
- Flask input form
- Flask model prediction
- Prediction result display
- Scenario comparison with CDC and CANRISK

Next steps:

- Finalize README and documentation
- Complete Power BI visuals
- Record the MidCourse demonstration video
- Complete the final report and presentation
