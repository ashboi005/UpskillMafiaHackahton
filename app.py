from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+psycopg2://default:SA57KMxEhzwb@ep-holy-firefly-a1hm97ya.ap-southeast-1.aws.neon.tech:5432/verceldb?sslmode=require"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'login'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

class Ragpicker(db.Model):
    __tablename__ = 'ragpicker_login'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

class UserDetails(db.Model):
    __tablename__ = 'user_details'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('login.id'), nullable=False)
    name = db.Column(db.String(100))
    phone_number = db.Column(db.String(20))
    email = db.Column(db.String(100))
    gender = db.Column(db.String(10))
    address = db.Column(db.String(200))
    city = db.Column(db.String(50))
    state = db.Column(db.String(50))
    pincode = db.Column(db.String(10))

    user = db.relationship('User', backref=db.backref('details', uselist=False))

class RagpickerDetails(db.Model):
    __tablename__ = 'ragpicker_details'

    id = db.Column(db.Integer, primary_key=True)
    ragpicker_id = db.Column(db.Integer, db.ForeignKey('ragpicker_login.id'), nullable=False)
    name = db.Column(db.String(100))
    contact_number = db.Column(db.String(20))
    locality = db.Column(db.String(100))
    city = db.Column(db.String(50))
    state = db.Column(db.String(50))
    pincode = db.Column(db.String(10))

    ragpicker = db.relationship('Ragpicker', backref=db.backref('details', uselist=False))

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if User.query.filter_by(username=username).first():
            return 'Username is already taken!'

        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            session['user_id'] = user.id
            return redirect(url_for('user_fill_details'))
        else:
            return 'Invalid username or password. Please try again.'

    return render_template('login.html')

@app.route('/ragpicker_register', methods=['GET', 'POST'])
def ragpicker_register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if Ragpicker.query.filter_by(username=username).first():
            return 'Username is already taken!'

        new_ragpicker = Ragpicker(username=username, password=password)
        db.session.add(new_ragpicker)
        db.session.commit()

        return redirect(url_for('ragpicker_login'))

    return render_template('ragpicker_register.html')

@app.route('/ragpicker_login', methods=['GET', 'POST'])
def ragpicker_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        ragpicker = Ragpicker.query.filter_by(username=username).first()

        if ragpicker and ragpicker.password == password:
            session['ragpicker_id'] = ragpicker.id
            session['user_type'] = 'ragpicker'
            return redirect(url_for('ragpicker_fill_details'))
        else:
            return 'Invalid username or password. Please try again.'

    return render_template('ragpicker_login.html')

@app.route('/ragpicker_fill_details', methods=['GET', 'POST'])
def ragpicker_fill_details():
    if 'ragpicker_id' not in session:
        return redirect(url_for('ragpicker_login'))

    ragpicker_details = RagpickerDetails.query.filter_by(ragpicker_id=session['ragpicker_id']).first()

    if request.method == 'POST':
        if not ragpicker_details:
            ragpicker_details = RagpickerDetails(ragpicker_id=session['ragpicker_id'])
            db.session.add(ragpicker_details)

        ragpicker_details.name = request.form['name']
        ragpicker_details.contact_number = request.form['contact_number']
        ragpicker_details.locality = request.form['locality']
        ragpicker_details.city = request.form['city']
        ragpicker_details.state = request.form['state']
        ragpicker_details.pincode = request.form['pincode']

        db.session.commit()

        return redirect(url_for('ragpicker_dashboard'))

    return render_template('ragpicker_fill_details.html', ragpicker_details=ragpicker_details)

@app.route('/ragpicker_dashboard')
def ragpicker_dashboard():
    if 'ragpicker_id' not in session:
        return redirect(url_for('ragpicker_login'))

    ragpicker_details = RagpickerDetails.query.filter_by(ragpicker_id=session['ragpicker_id']).first()
    return render_template('ragpicker_dashboard.html', ragpicker_details=ragpicker_details)

@app.route('/user_fill_details', methods=['GET', 'POST'])
def user_fill_details():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_details = UserDetails.query.filter_by(user_id=session['user_id']).first()

    if request.method == 'POST':
        if not user_details:
            user_details = UserDetails(user_id=session['user_id'])
            db.session.add(user_details)

        user_details.name = request.form['name']
        user_details.phone_number = request.form['phone_number']
        user_details.email = request.form['email']
        user_details.gender = request.form['gender']
        user_details.address = request.form['address']
        user_details.city = request.form['city']
        user_details.state = request.form['state']
        user_details.pincode = request.form['pincode']

        db.session.commit()

        return redirect(url_for('user_dashboard'))

    return render_template('user_fill_details.html', user_details=user_details)

@app.route('/user_dashboard')
def user_dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_details = UserDetails.query.filter_by(user_id=session['user_id']).first()
    return render_template('user_dashboard.html', user_details=user_details)

if __name__ == '__main__':
    app.run()
