from flask import Flask, render_template, request, redirect, session, url_for
import pandas as pd
import joblib

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load trained model
model = joblib.load('model.pkl')

# Expected columns as per model training
EXPECTED_COLUMNS = [
    'age', 'hypertension', 'heart_disease', 'bmi', 'HbA1c_level', 'blood_glucose_level',
    'gender_Female', 'gender_Male',
    'smoking_history_current', 'smoking_history_non-smoker', 'smoking_history_past_smoker'
]

@app.route('/')
def index():
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['user'] = request.form['username']
        return redirect('/dashboard')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user' not in session:
        return redirect('/login')

    result = None

    if request.method == 'POST':
        gender = request.form.get('gender')
        age = int(request.form.get('age') or 0)
        hypertension = int(request.form.get('hypertension') or 0)
        heart_disease = int(request.form.get('heart_disease') or 0)
        smoking_history = request.form.get('smoking_history')
        bmi = float(request.form.get('bmi') or 0)
        hba1c = float(request.form.get('hba1c') or 0)
        glucose = float(request.form.get('glucose') or 0)

        # Prepare raw input
        raw = {
            'gender': gender,
            'age': age,
            'hypertension': hypertension,
            'heart_disease': heart_disease,
            'smoking_history': smoking_history,
            'bmi': bmi,
            'HbA1c_level': hba1c,
            'blood_glucose_level': glucose
        }

        df = pd.DataFrame([raw])

        # One-hot encode gender and smoking_history
        df = pd.get_dummies(df, columns=['gender', 'smoking_history'])

        # Ensure all expected columns exist
        for col in EXPECTED_COLUMNS:
            if col not in df.columns:
                df[col] = 0

        # Reorder columns to match model input
        df = df[EXPECTED_COLUMNS]

        # Predict
        prediction = model.predict(df)[0]
        result = "Positive" if prediction == 1 else "Negative"

    return render_template('dashboard.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
