import streamlit as st
import pandas as pd
import joblib

st.title("🎓 Student Grade Predictor")

# Load model
try:
    model = joblib.load("best_model.pkl")
except Exception as e:
    st.error(f"Error loading model: {e}")
    st.stop()

# === Input Fields ===

# Numeric Inputs
age = st.number_input("Age", min_value=15, max_value=25, value=17)
Medu = st.slider("Mother's Education (0–4)", 0, 4, 2)
Fedu = st.slider("Father's Education (0–4)", 0, 4, 2)
traveltime = st.slider("Travel Time (1–4)", 1, 4, 1)
studytime = st.slider("Study Time (1–4)", 1, 4, 2)
failures = st.slider("Number of Past Failures", 0, 3, 0)
famrel = st.slider("Family Relationship Quality (1–5)", 1, 5, 4)
freetime = st.slider("Free Time (1–5)", 1, 5, 3)
goout = st.slider("Going Out with Friends (1–5)", 1, 5, 3)
Dalc = st.slider("Workday Alcohol Use (1–5)", 1, 5, 1)
Walc = st.slider("Weekend Alcohol Use (1–5)", 1, 5, 2)
health = st.slider("Health Status (1–5)", 1, 5, 3)
absences = st.number_input("Absences", 0, 100, 4)
G1 = st.slider("First Period Grade (0–20)", 0, 20, 12)
G2 = st.slider("Second Period Grade (0–20)", 0, 20, 13)

# Binary/Categorical Encoded as 0/1
school_MS = st.checkbox("School: MS?")
sex_M = st.checkbox("Gender: Male?")
address_U = st.checkbox("Address: Urban?")
famsize_LE3 = st.checkbox("Family Size: <= 3?")
Pstatus_T = st.checkbox("Parents living together?")

# One-hot encoded job/guardian/reason
Mjob = st.selectbox("Mother's Job", ["health", "other", "services", "teacher"])
Fjob = st.selectbox("Father's Job", ["health", "other", "services", "teacher"])
reason = st.selectbox("Reason for Choosing School", ["home", "other", "reputation"])
guardian = st.selectbox("Guardian", ["mother", "other"])

# More binary features
schoolsup_yes = st.checkbox("School Support?")
famsup_yes = st.checkbox("Family Support?")
paid_yes = st.checkbox("Extra Paid Classes?")
activities_yes = st.checkbox("Extra-curricular Activities?")
nursery_yes = st.checkbox("Attended Nursery?")
higher_yes = st.checkbox("Wants Higher Education?")
internet_yes = st.checkbox("Has Internet Access?")
romantic_yes = st.checkbox("In a Romantic Relationship?")

# Create input DataFrame
input_dict = {
    'age': age, 'Medu': Medu, 'Fedu': Fedu, 'traveltime': traveltime, 'studytime': studytime,
    'failures': failures, 'famrel': famrel, 'freetime': freetime, 'goout': goout, 'Dalc': Dalc,
    'Walc': Walc, 'health': health, 'absences': absences, 'G1': G1, 'G2': G2,
    'school_MS': int(school_MS), 'sex_M': int(sex_M), 'address_U': int(address_U),
    'famsize_LE3': int(famsize_LE3), 'Pstatus_T': int(Pstatus_T),
    'Mjob_health': 0, 'Mjob_other': 0, 'Mjob_services': 0, 'Mjob_teacher': 0,
    'Fjob_health': 0, 'Fjob_other': 0, 'Fjob_services': 0, 'Fjob_teacher': 0,
    'reason_home': 0, 'reason_other': 0, 'reason_reputation': 0,
    'guardian_mother': 0, 'guardian_other': 0,
    'schoolsup_yes': int(schoolsup_yes), 'famsup_yes': int(famsup_yes),
    'paid_yes': int(paid_yes), 'activities_yes': int(activities_yes),
    'nursery_yes': int(nursery_yes), 'higher_yes': int(higher_yes),
    'internet_yes': int(internet_yes), 'romantic_yes': int(romantic_yes),
}

# One-hot encode selected values
input_dict[f"Mjob_{Mjob}"] = 1
input_dict[f"Fjob_{Fjob}"] = 1
input_dict[f"reason_{reason}"] = 1
input_dict[f"guardian_{guardian}"] = 1

# Convert to DataFrame
input_df = pd.DataFrame([input_dict])

# Predict
if st.button("Predict Final Grade (G3)"):
    try:
        prediction = model.predict(input_df)
        st.success(f"🎯 Predicted Final Grade (G3): {round(prediction[0], 2)}")
    except Exception as e:
        st.error(f"Prediction failed: {e}")
