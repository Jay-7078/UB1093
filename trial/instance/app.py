from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "secret123"

# ===============================
# DATABASE CONFIG
# ===============================
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ===============================
# DATABASE MODELS
# ===============================
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    medicines = db.relationship('Medicine', backref='user', lazy=True)
    health_records = db.relationship('Health', backref='user', lazy=True)

class Medicine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    dosage = db.Column(db.String(50), nullable=False)
    time = db.Column(db.String(10), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Health(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bp = db.Column(db.String(20))
    sugar = db.Column(db.String(20))
    heart_rate = db.Column(db.String(10))
    weight = db.Column(db.String(20))
    date = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# ===============================
# LOGIN
# ===============================
@app.route('/', methods=['GET','POST'])
def login():
    if session.get('logged_in'):
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session['logged_in'] = True
            session['email'] = user.email
            session['user_id'] = user.id
            flash("Login successful!", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid Email or Password", "danger")

    return render_template('login.html')

# ===============================
# REGISTER
# ===============================
@app.route('/register', methods=['GET','POST'])
def register():
    if session.get('logged_in'):
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if User.query.filter_by(email=email).first():
            flash("Email already exists!", "warning")
        else:
            hashed_password = generate_password_hash(password)
            new_user = User(email=email, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash("Account created! Please login.", "success")
            return redirect(url_for('login'))

    return render_template('register.html')

# ===============================
# DASHBOARD (HEALTH)
# ===============================
@app.route('/dashboard', methods=['GET','POST'])
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    user_id = session.get('user_id')

    if request.method == 'POST':
        record = Health(
            bp=request.form.get('bp'),
            sugar=request.form.get('sugar'),
            heart_rate=request.form.get('heart_rate'),
            weight=request.form.get('weight'),
            user_id=user_id
        )
        db.session.add(record)
        db.session.commit()
        flash("Health record added!", "success")
        return redirect(url_for('dashboard'))

    health = Health.query.filter_by(user_id=user_id).order_by(Health.date.desc()).all()
    recommendation = "No health data available"

    if health:
        latest = health[0]
        try:
            if latest.bp and int(latest.bp) > 140:
                recommendation = "⚠️ Blood pressure is high. Reduce salt & relax."
            elif latest.sugar and int(latest.sugar) > 180:
                recommendation = "⚠️ Sugar level high. Avoid sweets & walk daily."
            elif latest.heart_rate and int(latest.heart_rate) > 100:
                recommendation = "⚠️ Heart rate high. Take rest and stay calm."
            elif latest.weight and int(latest.weight) < 45:
                recommendation = "⚠️ Weight is low. Eat nutritious food."
            else:
                recommendation = "✅ Health looks good. Keep maintaining!"
        except ValueError:
            recommendation = "⚠️ Invalid health data format."

    return render_template('dashboard.html', health=health, recommendation=recommendation)

# ===============================
# MEDICINE RECORDS
# ===============================
@app.route('/records', methods=['GET','POST'])
def records():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    user_id = session.get('user_id')

    if request.method == 'POST':
        name = request.form.get('name')
        dosage = request.form.get('dosage')
        time = request.form.get('time')

        if name and dosage and time:
            med = Medicine(name=name, dosage=dosage, time=time, user_id=user_id)
            db.session.add(med)
            db.session.commit()
            flash("Medicine added!", "success")
        else:
            flash("Please fill all fields!", "warning")
        return redirect(url_for('records'))

    medicines = Medicine.query.filter_by(user_id=user_id).all()
    return render_template('records.html', medicines=medicines)

# ===============================
# DELETE ROUTES
# ===============================
@app.route('/delete_medicine/<int:id>')
def delete_medicine(id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    user_id = session.get('user_id')
    med = Medicine.query.filter_by(id=id, user_id=user_id).first_or_404()
    db.session.delete(med)
    db.session.commit()
    flash("Medicine deleted!", "info")
    return redirect(url_for('records'))

@app.route('/delete_health/<int:id>')
def delete_health(id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    user_id = session.get('user_id')
    record = Health.query.filter_by(id=id, user_id=user_id).first_or_404()
    db.session.delete(record)
    db.session.commit()
    flash("Health record deleted!", "info")
    return redirect(url_for('dashboard'))

# ===============================
# PROFILE & PASSWORD
# ===============================
@app.route('/profile')
def profile():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    user = User.query.filter_by(email=session.get('email')).first()
    return render_template('profile.html', user=user)

@app.route('/change_password', methods=['GET','POST'])
def change_password():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    user = User.query.filter_by(email=session.get('email')).first()

    if request.method == 'POST':
        old = request.form.get('old_password')
        new = request.form.get('new_password')

        if check_password_hash(user.password, old):
            user.password = generate_password_hash(new)
            db.session.commit()
            flash("Password updated successfully!", "success")
            return redirect(url_for('profile'))
        else:
            flash("Old password incorrect!", "danger")

    return render_template('change_password.html')

# ===============================
# STATIC PAGES
# ===============================
@app.route('/help')
def help_page():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('help.html')

@app.route('/settings')
def settings():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('settings.html')

# ===============================
# LOGOUT
# ===============================
@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully!", "info")
    return redirect(url_for('login'))

# ===============================
# MAIN
# ===============================
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)