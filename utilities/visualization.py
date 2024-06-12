import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('C:/Users/jwweg/PycharmProjects/heart_disease_app/patients.db')

# Query the data from the relevant table, assuming the table name is 'heart'
query = "SELECT * FROM patients"
data = pd.read_sql_query(query, conn)

# Close the connection
conn.close()

# List of numeric variables
numeric_vars = ['age', 'resting_blood_pressure', 'cholesterol', 'max_heart_rate_achieved', 'st_depression']

# List of categorical variables
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

# Remove the empty subplot for numeric variables
fig.delaxes(axes[-1])

# Adjust the spacing between the plots for numeric variables
fig.subplots_adjust(hspace=0.6, wspace=0.6)
plt.tight_layout()
plt.show()

# Set up the matplotlib figure for categorical variables
fig, axes = plt.subplots(nrows=4, ncols=2, figsize=(15, 20))
axes = axes.flatten()

# Plot each categorical variable
for i, var in enumerate(categorical_vars):
    sns.countplot(data=data, x=var, hue='target', ax=axes[i])
    axes[i].set_title(f'Distribution of {var} by Target')
    axes[i].legend(title='Target')

# Remove the empty subplot for categorical variables if the number of categorical variables is odd
if len(categorical_vars) % 2 != 0:
    fig.delaxes(axes[-1])

# Adjust the spacing between the plots for categorical variables
fig.subplots_adjust(hspace=0.6, wspace=0.6)
plt.tight_layout()
plt.show()