import numpy as np
import pandas as pd
import joblib
from sklearn.preprocessing import LabelEncoder

def load_label_encoders(file_path):
    with open(file_path, 'rb') as file:
        return joblib.load(file)

def is_already_encoded(column, value, label_encoder):
    try:
        label_encoder.inverse_transform([value])
        return True
    except ValueError:
        return False

def preprocess_patient_data(patient_data, label_encoders):
    # Convert example patient data to DataFrame
    patient_df = pd.DataFrame([patient_data])

    # Encode categorical features using the same encoders used during training
    for column, le in label_encoders.items():
        if column in patient_df:
            if not is_already_encoded(column, patient_df[column].iloc[0], le):
                patient_df[column] = le.transform(patient_df[column])
            else:
                print(f"{column} is already encoded as {patient_df[column].iloc[0]}")

    print("Preprocessed patient data:\n", patient_df)
    return patient_df

def predict_heart_disease(example_patient):
    # Load the best model from disk
    best_model_filename = "C:/Users/jwweg/PycharmProjects/heart_disease_app/utilities/best_model_logistic_regression.pkl"
    best_model = joblib.load(best_model_filename)

    # Load encoders
    label_encoders = load_label_encoders("C:/Users/jwweg/PycharmProjects/heart_disease_app/utilities/label_encoders.pkl")

    # Preprocess the patient data
    processed_patient_data = preprocess_patient_data(example_patient, label_encoders)

    # Predict the probability of heart disease
    probability = best_model.predict_proba(processed_patient_data)[:, 1]  # Probability of target = 1 (heart disease)
    print(f"Probability of heart disease: {probability[0]:.4f}")

# Example patient data
example_patient = {
    'age': 41,
    'sex': 0,
    'chest_pain_type': 1,
    'resting_blood_pressure': 130,
    'cholesterol': 204,
    'fasting_blood_sugar': 0,
    'rest_ecg': 0,
    'max_heart_rate_achieved': 172,
    'exercise_induced_angina': 0,
    'st_depression': 1,
    'st_slope': 2,
    'num_major_vessels': 0,
    'thalassemia': 2
}

# Main execution
if __name__ == "__main__":
    predict_heart_disease(example_patient)