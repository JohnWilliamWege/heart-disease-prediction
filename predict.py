import streamlit as st
import pandas as pd
import numpy as np
import joblib

def app():
    # Load the model, encoders, and min-max values
    best_model_filename = "C:/Users/jwweg/PycharmProjects/heart_disease_app/utilities/best_model_logistic_regression.pkl"
    best_model = joblib.load(best_model_filename)
    label_encoders = joblib.load("C:/Users/jwweg/PycharmProjects/heart_disease_app/utilities/label_encoders.pkl")
    min_max_values = pd.read_csv("C:/Users/jwweg/PycharmProjects/heart_disease_app/utilities/min_max_values.csv",
                                 index_col=0)

    # Define dictionaries for human-readable labels
    chest_pain_type_dict = {0: "Typical Angina", 1: "Atypical Angina", 2: "Non-Anginal Pain", 3: "Asymptomatic"}
    rest_ecg_dict = {0: "Normal", 1: "Having ST-T wave abnormality", 2: "Showing probable or definite left ventricular hypertrophy"}
    st_slope_dict = {0: "Upsloping", 1: "Flat", 2: "Downsloping"}
    thalassemia_dict = {0: "Normal", 1: "Fixed Defect", 2: "Reversible Defect"}

    # Define function to preprocess patient data
    def preprocess_patient_data(patient_data, label_encoders, min_max_values):
        patient_df = pd.DataFrame([patient_data])
        for column, le in label_encoders.items():
            if column in patient_df:
                if not is_already_encoded(column, patient_df[column].iloc[0], le):
                    try:
                        patient_df[column] = le.transform(patient_df[column])
                    except Exception as e:
                        st.write(f"Error encoding column {column}: {e}")
        numeric_features = patient_df.select_dtypes(include=[np.number]).columns
        for feature in numeric_features:
            if (min_max_values.loc[feature, 'max'] - min_max_values.loc[feature, 'min']) != 0:
                patient_df[feature] = (patient_df[feature] - min_max_values.loc[feature, 'min']) / (
                        min_max_values.loc[feature, 'max'] - min_max_values.loc[feature, 'min'])
            else:
                st.write(f"Feature {feature} has zero range during normalization.")
        return patient_df

    def is_already_encoded(column, value, label_encoder):
        try:
            label_encoder.inverse_transform([value])
            return True
        except ValueError:
            return False

    st.title("Heart Disease Prediction")
    age = st.number_input("Age", min_value=1, max_value=120, value=60)
    sex = st.selectbox("Sex", options=[0, 1], format_func=lambda x: "Female" if x == 0 else "Male")
    chest_pain_type = st.selectbox("Chest Pain Type", options=list(chest_pain_type_dict.keys()), format_func=lambda x: chest_pain_type_dict[x])
    resting_blood_pressure = st.number_input("Resting Blood Pressure", min_value=0, max_value=300, value=125)
    cholesterol = st.number_input("Cholesterol", min_value=0, max_value=1000, value=270)
    fasting_blood_sugar = st.selectbox("Fasting Blood Sugar > 120 mg/dl", options=[0, 1])
    rest_ecg = st.selectbox("Resting ECG", options=list(rest_ecg_dict.keys()), format_func=lambda x: rest_ecg_dict[x])
    max_heart_rate = st.number_input("Max Heart Rate Achieved", min_value=0, max_value=300, value=80)
    exercise_induced_angina = st.selectbox("Exercise Induced Angina", options=[0, 1], format_func=lambda x: "No" if x == 0 else "Yes")
    st_depression = st.number_input("ST Depression", min_value=0.0, max_value=10.0, value=0.2, step=0.1)
    st_slope = st.selectbox("ST Slope", options=list(st_slope_dict.keys()), format_func=lambda x: st_slope_dict[x])
    num_major_vessels = st.number_input("Number of Major Vessels", min_value=0, max_value=4, value=0)
    thalassemia = st.selectbox("Thalassemia", options=list(thalassemia_dict.keys()), format_func=lambda x: thalassemia_dict[x])

    def generate_report(probability):
        if probability > 0.5:
            return (
                "The patient is at risk of heart disease with a probability of "
                f"{probability:.2f} ({probability * 100:.2f}%). It is strongly recommended "
                "that the patient seeks further testing and consultation with a healthcare professional."
            )
        else:
            return (
                "The patient has a low probability of heart disease with a probability of "
                f"{probability:.2f} ({probability * 100:.2f}%). Regular check-ups and a healthy lifestyle "
                "are recommended to maintain good heart health."
            )

    if st.button("Predict"):
        example_patient = {
            'age': age,
            'sex': sex,
            'chest_pain_type': chest_pain_type,
            'resting_blood_pressure': resting_blood_pressure,
            'cholesterol': cholesterol,
            'fasting_blood_sugar': fasting_blood_sugar,
            'rest_ecg': rest_ecg,
            'max_heart_rate_achieved': max_heart_rate,
            'exercise_induced_angina': exercise_induced_angina,
            'st_depression': st_depression,
            'st_slope': st_slope,
            'num_major_vessels': num_major_vessels,
            'thalassemia': thalassemia
        }

        processed_patient_data = preprocess_patient_data(example_patient, label_encoders, min_max_values)

        st.write("Example Patient Data:", example_patient)
        st.write("Processed Patient Data:", processed_patient_data)

        if processed_patient_data.isnull().values.any():
            st.write("Processed data contains NaN values. Columns with NaN values are:")
            st.write(processed_patient_data.isnull().sum()[processed_patient_data.isnull().sum() > 0])
        else:
            try:
                probability = best_model.predict_proba(processed_patient_data)[:, 1][0]
                st.write("Prediction Probability:", probability)
                st.write(f"Probability of heart disease: {probability:.4f} ({probability * 100:.2f}%)")
                report = generate_report(probability)
                st.write(report)
            except ValueError as e:
                st.write(f"Error in prediction: {e}")




if __name__ == "__main__":
    app()
