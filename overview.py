import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
def app():
    st.title("Patient Data Overview")

    def load_data(db_path):
        conn = sqlite3.connect(db_path)
        myData = pd.read_sql_query("SELECT * FROM patients", conn)
        conn.close()
        return myData

    def analyze_age_heart_disease_relationship(data):
        correlation = data['age'].corr(data['target'])
        st.write(f"Correlation coefficient between age and heart disease: {correlation:.4f}")

        bins = [29, 39, 49, 59, 69, 79, 89, 99]
        labels = ['30-39', '40-49', '50-59', '60-69', '70-79', '80-89', '90-99']
        data['age_group'] = pd.cut(data['age'], bins=bins, labels=labels, right=False)

        plt.figure(figsize=(10, 6))
        sns.barplot(x='age_group', y='target', data=data, ci=None)
        plt.title('Bar Plot of Age Group vs Heart Disease')
        plt.xlabel('Age Group')
        plt.ylabel('Average Heart Disease Occurrence (1 = Yes, 0 = No)')
        st.pyplot(plt)

    db_path = os.path.join(current_dir, 'patients.db')
    data = load_data(db_path)
    st.write("### Patient Data", data)

    analyze_age_heart_disease_relationship(data)

    numeric_vars = ['age', 'resting_blood_pressure', 'cholesterol', 'max_heart_rate_achieved', 'st_depression']
    categorical_vars = ['sex', 'chest_pain_type', 'fasting_blood_sugar', 'rest_ecg', 'exercise_induced_angina', 'st_slope', 'num_major_vessels', 'thalassemia']

    st.write("### Numeric Features Distribution by Target")
    fig, axes = plt.subplots(nrows=3, ncols=2, figsize=(15, 15))
    axes = axes.flatten()
    for i, var in enumerate(numeric_vars):
        sns.histplot(data=data, x=var, hue='target', element="step", stat="density", common_norm=False, ax=axes[i])
        axes[i].set_title(f'Distribution of {var} by Target')
        mean_no_heart_disease = data[data['target'] == 0][var].mean()
        mean_heart_disease = data[data['target'] == 1][var].mean()
        axes[i].axvline(mean_no_heart_disease, color='blue', linestyle='dashed', linewidth=2, label='No Heart Disease Avg')
        axes[i].axvline(mean_heart_disease, color='orange', linestyle='dashed', linewidth=2, label='Heart Disease Avg')
        axes[i].legend(title='Target')
    fig.delaxes(axes[-1])
    fig.subplots_adjust(hspace=0.6, wspace=0.6)
    st.pyplot(fig)

    st.write("### Categorical Features Distribution by Target")
    fig, axes = plt.subplots(nrows=4, ncols=2, figsize=(15, 20))
    axes = axes.flatten()
    for i, var in enumerate(categorical_vars):
        sns.countplot(data=data, x=var, hue='target', ax=axes[i])
        axes[i].set_title(f'Distribution of {var} by Target')
        axes[i].legend(title='Target')
    if len(categorical_vars) % 2 != 0:
        fig.delaxes(axes[-1])
    fig.subplots_adjust(hspace=0.6, wspace=0.6)
    st.pyplot(fig)