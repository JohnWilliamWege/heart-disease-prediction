import pandas as pd
import sqlite3
import seaborn as sns
import matplotlib.pyplot as plt


def load_data(db_path):
    conn = sqlite3.connect(db_path)
    myData = pd.read_sql_query("SELECT * FROM patients", conn)
    conn.close()
    return myData


def analyze_age_heart_disease_relationship(db_path):
    # Load the data
    myData = load_data(db_path)

    # Calculate the correlation coefficient
    correlation = myData['age'].corr(myData['target'])
    print(f"Correlation coefficient between age and heart disease: {correlation:.4f}")

    # Create age bins
    bins = [29, 39, 49, 59, 69, 79, 89, 99]
    labels = ['30-39', '40-49', '50-59', '60-69', '70-79', '80-89', '90-99']
    myData['age_group'] = pd.cut(myData['age'], bins=bins, labels=labels, right=False)

    # Create a bar plot
    plt.figure(figsize=(10, 6))
    sns.barplot(x='age_group', y='target', data=myData, ci=None)
    plt.title('Bar Plot of Age Group vs Heart Disease')
    plt.xlabel('Age Group')
    plt.ylabel('Average Heart Disease Occurrence (1 = Yes, 0 = No)')
    plt.show()


# Example execution
db_path = 'C:/Users/jwweg/PycharmProjects/heart_disease_app/patients.db'
analyze_age_heart_disease_relationship(db_path)
