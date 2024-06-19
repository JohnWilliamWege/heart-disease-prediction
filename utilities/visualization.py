import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('C:/Users/jwweg/PycharmProjects/heart_disease_app/patients.db')

# Query for data
query = "SELECT * FROM patients"
data = pd.read_sql_query(query, conn)

conn.close()

# List of the  numerical variables
numeric_vars = ['age', 'resting_blood_pressure', 'cholesterol', 'max_heart_rate_achieved', 'st_depression']

# List of the categorical variables
categorical_vars = ['sex', 'chest_pain_type', 'fasting_blood_sugar', 'rest_ecg', 'exercise_induced_angina', 'st_slope', 'num_major_vessels', 'thalassemia']

# Set up the matplotlib figure for numeric variables
fig, axes = plt.subplots(nrows=3, ncols=2, figsize=(15, 15))
axes = axes.flatten()

# Plot each numeric variable
for i, var in enumerate(numeric_vars):
    sns.histplot(data=data, x=var, hue='target', element="step", stat="density", common_norm=False, ax=axes[i])
    axes[i].set_title(f'Distribution of {var} by Target')

    # Calculate and plot the average lines for each target group
    mean_no_heart_disease = data[data['target'] == 0][var].mean()
    mean_heart_disease = data[data['target'] == 1][var].mean()
    axes[i].axvline(mean_no_heart_disease, color='blue', linestyle='dashed', linewidth=2, label='No Heart Disease Avg')
    axes[i].axvline(mean_heart_disease, color='orange', linestyle='dashed', linewidth=2, label='Heart Disease Avg')
    axes[i].legend(title='Target')

# Remove the empty subplot if necessary
if len(numeric_vars) < len(axes):
    fig.delaxes(axes[len(numeric_vars)])

# Adjust the spacing between the plots for numeric variables
fig.subplots_adjust(hspace=0.5, wspace=0.4)
plt.tight_layout()
plt.show()

# Set up figure for categorical variables using matplotlib library
fig, axes = plt.subplots(nrows=4, ncols=2, figsize=(12, 16))
axes = axes.flatten()

# Plot each categorical variable
for i, var in enumerate(categorical_vars):
    sns.countplot(data=data, x=var, hue='target', ax=axes[i])
    axes[i].set_title(f'Distribution of {var} by Target')
    axes[i].legend(title='Target')

# Remove the empty subplot for categorical variables if necessary
if len(categorical_vars) < len(axes):
    fig.delaxes(axes[len(categorical_vars)])

# Adjust the spacing
fig.subplots_adjust(hspace=1, wspace=0.4)
plt.tight_layout()
plt.show()