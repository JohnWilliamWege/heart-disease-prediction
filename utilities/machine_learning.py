import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
import sqlite3
import joblib
import os

def save_label_encoders(label_encoders, file_path):
    with open(file_path, 'wb') as file:
        joblib.dump(label_encoders, file)

def load_label_encoders(file_path):
    with open(file_path, 'rb') as file:
        return joblib.load(file)

def save_min_max_values(x_train, file_path):
    min_values = x_train.min()
    max_values = x_train.max()
    min_max_values = pd.DataFrame({"min": min_values, "max": max_values})
    min_max_values.to_csv(file_path)

def load_and_preprocess_data(db_path):
    # Connect to database
    conn = sqlite3.connect(db_path)
    myData = pd.read_sql_query("SELECT * FROM patients", conn)
    conn.close()

    if 'id' in myData.columns:
        myData = myData.drop(columns=['id'])

    # Convert categorical text values back to numerical codes
    label_encoders = {}
    for column in ['sex', 'chest_pain_type', 'fasting_blood_sugar', 'rest_ecg',
                   'exercise_induced_angina', 'st_slope', 'thalassemia']:
        le = LabelEncoder()
        myData[column] = le.fit_transform(myData[column])
        label_encoders[column] = le

    save_label_encoders(label_encoders, "label_encoders.pkl")

    # Split the data
    x = myData.drop('target', axis=1)
    y = myData['target']

    # Perform train/test splitting
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

    # Save min and max values using only the training set
    numeric_features = x_train.select_dtypes(include=[np.number]).columns
    min_max_values = pd.DataFrame({"min": x_train[numeric_features].min(), "max": x_train[numeric_features].max()})
    min_max_values.to_csv("min_max_values.csv")

    # Normalize the training and testing data using the saved min and max values
    for feature in numeric_features:
        x_train[feature] = (x_train[feature] - min_max_values.loc[feature, 'min']) / (
                min_max_values.loc[feature, 'max'] - min_max_values.loc[feature, 'min'])
        x_test[feature] = (x_test[feature] - min_max_values.loc[feature, 'min']) / (
                min_max_values.loc[feature, 'max'] - min_max_values.loc[feature, 'min'])

    return x_train, x_test, y_train, y_test

def print_cv_scores(model_name, cv_scores):
    print(f"{model_name} Cross-Validation Scores: {cv_scores}")
    print(f"Average {model_name} Cross-Validation Accuracy: {np.mean(cv_scores):.4f}")

def logistic_regression_model(x_train, y_train, print_cv=True):
    lin_model = LogisticRegression(solver='lbfgs', max_iter=1000)
    if print_cv:
        cv_scores = cross_val_score(lin_model, x_train, y_train, cv=5)
        print_cv_scores("Logistic Regression", cv_scores)
    lin_model.fit(x_train, y_train)
    return lin_model

def knn_model(x_train, y_train, print_cv=True):
    knn = KNeighborsClassifier()
    if print_cv:
        cv_scores = cross_val_score(knn, x_train, y_train, cv=5)
        print_cv_scores("K Nearest Neighbor", cv_scores)
    knn.fit(x_train, y_train)
    return knn

def decision_tree_model(x_train, y_train, print_cv=True):
    dt_model = DecisionTreeClassifier(max_depth=5, min_samples_split=10)
    if print_cv:
        cv_scores = cross_val_score(dt_model, x_train, y_train, cv=5)
        print_cv_scores("Decision Tree", cv_scores)
    dt_model.fit(x_train, y_train)
    return dt_model

def evaluate_models():
    # Load and preprocess data
    db_path = 'C:/Users/jwweg/PycharmProjects/heart_disease_app/patients.db'
    x_train, x_test, y_train, y_test = load_and_preprocess_data(db_path)

    # Evaluate models
    print("Evaluating models with cross-validation...\n")
    lin_model = logistic_regression_model(x_train, y_train)
    knn = knn_model(x_train, y_train)
    dt_model = decision_tree_model(x_train, y_train)

    # Evaluate on test set
    print("\nEvaluating models on the test set...\n")
    lin_accuracy = lin_model.score(x_test, y_test)
    print(f"Logistic Regression Test Accuracy: {lin_accuracy:.4f}")

    knn_accuracy = knn.score(x_test, y_test)
    print(f"K Nearest Neighbor Test Accuracy: {knn_accuracy:.4f}")

    dt_accuracy = dt_model.score(x_test, y_test)
    print(f"Decision Tree Test Accuracy: {dt_accuracy:.4f}")

    # Determine best model (excluding Decision Tree)
    accuracies = {"Logistic Regression": lin_accuracy, "K Nearest Neighbor": knn_accuracy}
    best_model_name = max(accuracies, key=accuracies.get)
    best_model = {"Logistic Regression": lin_model, "K Nearest Neighbor": knn}[best_model_name]
    print(f"\nBest model is: {best_model_name} with accuracy: {accuracies[best_model_name]:.4f}")

    # Save the best model to disk
    joblib.dump(best_model, f"best_model_{best_model_name.replace(' ', '_').lower()}.pkl")
    print(f"Best model saved to disk as best_model_{best_model_name.replace(' ', '_').lower()}.pkl")

# Main execution
evaluate_models()