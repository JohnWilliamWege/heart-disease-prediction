

import pandas as pd
import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('C:/Users/jwweg/PycharmProjects/heart_disease_app/patients.db')


# Read data from the database into a DataFrame
query = "SELECT * FROM patients"
pdf = pd.read_sql_query(query, conn)

# Rename columns for better readability
pdf.columns = [
    'id', 'age', 'sex', 'chest_pain_type', 'resting_blood_pressure', 'cholesterol',
    'fasting_blood_sugar', 'rest_ecg', 'max_heart_rate_achieved',
    'exercise_induced_angina', 'st_depression', 'st_slope', 'num_major_vessels',
    'thalassemia', 'target'
]

# Map the categorical values to more descriptive names
pdf['sex'] = pdf['sex'].map({0: 'female', 1: 'male'})
pdf['chest_pain_type'] = pdf['chest_pain_type'].map({
    0: 'typical angina',
    1: 'atypical angina',
    2: 'non-anginal pain',
    3: 'asymptomatic'
})
pdf['fasting_blood_sugar'] = pdf['fasting_blood_sugar'].map({
    0: 'lower than 120mg/ml',
    1: 'greater than 120mg/ml'
})
pdf['rest_ecg'] = pdf['rest_ecg'].map({
    0: 'normal',
    1: 'ST-T wave abnormality',
    2: 'left ventricular hypertrophy'
})
pdf['exercise_induced_angina'] = pdf['exercise_induced_angina'].map({
    0: 'no',
    1: 'yes'
})
pdf['st_slope'] = pdf['st_slope'].map({
    0: 'upsloping',
    1: 'flat',
    2: 'downsloping'
})
pdf['thalassemia'] = pdf['thalassemia'].map({
    0: 'unknown',
    1: 'normal',
    2: 'fixed defect',
    3: 'reversible defect'

})

# Display the first few rows to verify the changes
print(pdf.head())

# Update the database with the processed data
pdf.to_sql('patients', conn, if_exists='replace', index=False)

# Close the connection
conn.close()