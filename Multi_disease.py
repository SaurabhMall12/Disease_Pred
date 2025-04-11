# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 12:11:56 2025

@author: Saurabh
"""

import os
import pickle
import streamlit as st
from streamlit_option_menu import option_menu
from pyairtable import Table
from datetime import datetime

# Set page configuration
st.set_page_config(page_title="Health Assistant",
                   layout="wide",
                   page_icon="🧑‍⚕️")

# Cache models
@st.cache_resource
def load_diabetes_model():
    return pickle.load(open(os.path.join('saved_models', 'diabetes_model.sav'), 'rb'))

@st.cache_resource
def load_heart_model():
    return pickle.load(open(os.path.join('saved_models', 'heart_disease_model.sav'), 'rb'))

@st.cache_resource
def load_parkinsons_model():
    return pickle.load(open(os.path.join('saved_models', 'parkinsons_model.sav'), 'rb'))

# Load models
with st.spinner("Loading models..."):
    diabetes_model = load_diabetes_model()
    heart_disease_model = load_heart_model()
    parkinsons_model = load_parkinsons_model()

# Sidebar navigation
with st.sidebar:
    selected = option_menu('Chronic Disease Prediction System',
                           ['Diabetes Prediction', 'Heart Disease Prediction', 'Parkinsons Prediction'],
                           menu_icon='hospital-fill',
                           icons=['activity', 'heart', 'person'],
                           default_index=0)

# Diabetes Prediction
if selected == 'Diabetes Prediction':
    st.title('Diabetes Prediction using ML')
    col1, col2, col3 = st.columns(3)
    with col1: Pregnancies = st.number_input('Number of Pregnancies', step=1.0)
    with col2: Glucose = st.number_input('Glucose Level', step=1.0)
    with col3: BloodPressure = st.number_input('Blood Pressure value', step=1.0)
    with col1: SkinThickness = st.number_input('Skin Thickness value', step=1.0)
    with col2: Insulin = st.number_input('Insulin Level', step=1.0)
    with col3: BMI = st.number_input('BMI value', step=0.1)
    with col1: DiabetesPedigreeFunction = st.number_input('Diabetes Pedigree Function value', step=0.01)
    with col2: Age = st.number_input('Age of the Person', step=1.0)
    diab_diagnosis = ''
    if st.button('Diabetes Test Result'):
        user_input = [Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age]
        diab_prediction = diabetes_model.predict([user_input])
        diab_diagnosis = 'The person is diabetic' if diab_prediction[0] == 1 else 'The person is not diabetic'
    st.success(diab_diagnosis)

# Heart Disease Prediction
if selected == 'Heart Disease Prediction':
    st.title('Heart Disease Prediction using ML')
    col1, col2, col3 = st.columns(3)
    with col1: age = st.number_input('Age', step=1.0)
    with col2: sex = st.number_input('Sex', step=1.0)
    with col3: cp = st.number_input('Chest Pain types', step=1.0)
    with col1: trestbps = st.number_input('Resting Blood Pressure', step=1.0)
    with col2: chol = st.number_input('Serum Cholestoral in mg/dl', step=1.0)
    with col3: fbs = st.number_input('Fasting Blood Sugar > 120 mg/dl', step=1.0)
    with col1: restecg = st.number_input('Resting Electrocardiographic results', step=1.0)
    with col2: thalach = st.number_input('Maximum Heart Rate achieved', step=1.0)
    with col3: exang = st.number_input('Exercise Induced Angina', step=1.0)
    with col1: oldpeak = st.number_input('ST depression induced by exercise', step=0.1)
    with col2: slope = st.number_input('Slope of the peak exercise ST segment', step=1.0)
    with col3: ca = st.number_input('Major vessels colored by flourosopy', step=1.0)
    with col1: thal = st.number_input('thal: 0 = normal; 1 = fixed defect; 2 = reversable defect', step=1.0)
    heart_diagnosis = ''
    if st.button('Heart Disease Test Result'):
        user_input = [age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]
        heart_prediction = heart_disease_model.predict([user_input])
        heart_diagnosis = 'The person is having heart disease' if heart_prediction[0] == 1 else 'The person does not have any heart disease'
    st.success(heart_diagnosis)

# Parkinson's Prediction
if selected == "Parkinsons Prediction":
    st.title("Parkinson's Disease Prediction using ML")
    inputs = [st.number_input(label, step=0.001) for label in [
        'MDVP:Fo(Hz)', 'MDVP:Fhi(Hz)', 'MDVP:Flo(Hz)', 'MDVP:Jitter(%)', 'MDVP:Jitter(Abs)',
        'MDVP:RAP', 'MDVP:PPQ', 'Jitter:DDP', 'MDVP:Shimmer', 'MDVP:Shimmer(dB)',
        'Shimmer:APQ3', 'Shimmer:APQ5', 'MDVP:APQ', 'Shimmer:DDA', 'NHR', 'HNR',
        'RPDE', 'DFA', 'spread1', 'spread2', 'D2', 'PPE']]
    parkinsons_diagnosis = ''
    if st.button("Parkinson's Test Result"):
        parkinsons_prediction = parkinsons_model.predict([inputs])
        parkinsons_diagnosis = "The person has Parkinson's disease" if parkinsons_prediction[0] == 1 else "The person does not have Parkinson's disease"
    st.success(parkinsons_diagnosis)

# Review Section
st.markdown("---")
st.subheader("📝 Leave a Review")
name = st.text_input("Your Name")
review = st.text_area("Your Review")

AIRTABLE_TOKEN = st.secrets["AIRTABLE_TOKEN"]
AIRTABLE_BASE_ID = st.secrets["AIRTABLE_BASE_ID"]
AIRTABLE_TABLE_NAME = st.secrets["AIRTABLE_TABLE_NAME"]
table = Table(AIRTABLE_TOKEN, AIRTABLE_BASE_ID, AIRTABLE_TABLE_NAME)

if st.button("Submit Review"):
    if name and review:
        table.create({"Name": name, "Review": review, "Timestamp": datetime.now().isoformat()})
        st.success("✅ Thanks! Your review was saved.")
    else:
        st.warning("⚠️ Please fill out both fields.")

st.markdown("---")
st.subheader("📋 Recent Reviews")
records = list(reversed(table.all(sort=["Timestamp"])))
if records:
    for record in records[:5]:
        fields = record["fields"]
        st.text(f"{fields.get('Name', 'Anonymous')}: {fields.get('Review', '')} ({fields.get('Timestamp', '')})")
else:
    st.info("No reviews yet.")







