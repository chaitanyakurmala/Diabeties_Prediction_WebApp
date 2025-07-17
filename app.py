from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
from joblib import load

app = Flask(__name__)
app.secret_key = 'your_super_secret_key'

# MySQL config
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="diabetes_prediction"
)
cursor = db.cursor(dictionary=True)

# ---------- Login ----------
@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    login_failed = False

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        user = cursor.fetchone()

        if user:
            session['username'] = user['username']
            return redirect(url_for('dashboard'))
        else:
            login_failed = True

    return render_template('login.html', login_failed=login_failed)

# ---------- Registration ----------
@app.route('/register', methods=['GET', 'POST'])
def register():
    registration_success = False
    registration_failed = False

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        mobile = request.form.get('mobile')

        try:
            cursor.execute("INSERT INTO users (username, password, email, mobile) VALUES (%s, %s, %s, %s)",
                           (username, password, email, mobile))
            db.commit()
            registration_success = True
        except mysql.connector.IntegrityError:
            registration_failed = True

    return render_template("registration.html",
                           registration_success=registration_success,
                           registration_failed=registration_failed)

# ---------- Dashboard ----------
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))

    prediction_result = None
    gender = None

    if request.method == 'POST':
        model = load('model.pkl')

        gender = request.form.get('gender')
        pregnancies = int(request.form.get('pregnancies') or 0) if gender == 'female' else 0
        glucose = float(request.form.get('glucose') or 0)
        blood_pressure = float(request.form.get('blood_pressure') or 0)
        skin_thickness = float(request.form.get('skin_thickness') or 0)
        insulin = float(request.form.get('insulin') or 0)
        bmi = float(request.form.get('bmi') or 0)
        diabetes_pedigree = float(request.form.get('diabetes_pedigree') or 0)
        age = int(request.form.get('age') or 0)

        input_data = [[pregnancies, glucose, blood_pressure, skin_thickness, insulin, bmi, diabetes_pedigree, age]]
        prediction = model.predict(input_data)
        prediction_result = "Positive" if prediction[0] == 1 else "Negative"

    return render_template('dashboard.html',
                           username=session['username'],
                           result=prediction_result,
                           gender=gender)

# ---------- Logout ----------
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login.html'))

# ---------- Main ----------
if __name__ == '__main__':
    app.run(debug=True)
