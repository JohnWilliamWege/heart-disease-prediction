import pandas as pd
import numpy as np
import streamlit as st

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