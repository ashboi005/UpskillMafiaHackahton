from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
import os
import razorpay

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

class ContactFormSubmission(db.Model):
    __tablename__ = 'contact_form_submission'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

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

class ServiceRequest(db.Model):
    __tablename__ = 'service_requests'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('login.id'), nullable=False)
    ragpicker_id = db.Column(db.Integer, db.ForeignKey('ragpicker_login.id'), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    date_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    payment_status = db.Column(db.String(50), nullable=False, default='pending')  # new field

    user = db.relationship('User', backref=db.backref('service_requests', lazy=True))
    ragpicker = db.relationship('Ragpicker', backref=db.backref('service_requests', lazy=True))

class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('login.id'), nullable=False)
    ragpicker_id = db.Column(db.Integer, db.ForeignKey('ragpicker_login.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(500), nullable=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

    user = db.relationship('User', backref=db.backref('reviews', lazy=True))
    ragpicker = db.relationship('Ragpicker', backref=db.backref('reviews', lazy=True))

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit_contact_form', methods=['POST'])
def submit_contact_form():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')

    if not name or not email or not message:
        flash('All fields are required.', 'danger')
        return redirect(url_for('index'))

    # Optionally, you can store the submission in the database
    new_submission = ContactFormSubmission(name=name, email=email, message=message)
    db.session.add(new_submission)
    db.session.commit()

    flash('Thank you for your message. We will get back to you soon.', 'success')
    return redirect(url_for('index'))

@app.route('/choose_register')
def choose_register():
    return render_template('double_register.html')

@app.route('/choose_login')
def choose_login():
    return render_template('double_login.html')

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
            user_details = UserDetails.query.filter_by(user_id=user.id).first()
            if user_details:
                return redirect(url_for('user_dashboard'))
            else:
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
            ragpicker_details = RagpickerDetails.query.filter_by(ragpicker_id=ragpicker.id).first()
            if ragpicker_details:
                return redirect(url_for('ragpicker_dashboard'))
            else:
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
    service_requests = ServiceRequest.query.filter_by(ragpicker_id=session['ragpicker_id']).all()

    return render_template('ragpicker_dashboard.html', ragpicker_details=ragpicker_details)

@app.route('/service_requests')
def service_requests():
    service_requests_with_user_details = []
    for request in service_requests:
        user_details = UserDetails.query.filter_by(user_id=request.user_id).first()
        service_requests_with_user_details.append((request, user_details))

    return render_template('service_requests.html', service_requests_with_user_details=service_requests_with_user_details)

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
    service_requests = ServiceRequest.query.filter_by(user_id=session['user_id']).all()
    pending_payments = ServiceRequest.query.filter_by(user_id=session['user_id'], status='completed' , payment_status='pending').all()
    return render_template('user_dashboard.html', user_details=user_details, service_requests=service_requests, pending_payments=pending_payments)

@app.route('/book_service')
def book_service():
    ragpickers = RagpickerDetails.query.all()
    ragpicker_ratings = {}
    for ragpicker in ragpickers:
        avg_rating = db.session.query(db.func.avg(Review.rating)).filter_by(ragpicker_id=ragpicker.id).scalar()
        ragpicker_ratings[ragpicker.id] = round(avg_rating, 2) if avg_rating else 'No ratings yet'

    return render_template('book_service.html', ragpickers=ragpickers, ragpicker_ratings=ragpicker_ratings)

@app.route('/request_service/<int:ragpicker_id>', methods=['GET', 'POST'])
def request_service(ragpicker_id):
    ragpicker = RagpickerDetails.query.get_or_404(ragpicker_id)

    if request.method == 'POST':
        description = request.form['description']
        date_time = request.form['date_time']

        service_request = ServiceRequest(
            user_id=session['user_id'],
            ragpicker_id=ragpicker_id,
            description=description,
            date_time=date_time,
            status='pending'
        )
        db.session.add(service_request)
        db.session.commit()

        return redirect(url_for('user_dashboard'))

    return render_template('request_service.html', ragpicker=ragpicker)

@app.route('/update_service_request/<int:request_id>', methods=['POST'])
def update_service_request(request_id):
    service_request = ServiceRequest.query.get_or_404(request_id)
    action = request.form['action']

    if action == 'accept':
        service_request.status = 'accepted'
    elif action == 'reject':
        service_request.status = 'rejected'

    db.session.commit()
    return redirect(url_for('ragpicker_dashboard'))

@app.route('/payment/<int:request_id>', methods=['GET', 'POST'])
def payment(request_id):
    service_request = ServiceRequest.query.get_or_404(request_id)
    client = razorpay.Client(auth=("rzp_test_7zwfHYhy9Q3cZJ", "2WeEJ60cA83lrF2VjdYd8SHl"))
    payment = client.order.create({'amount': 50000, 'currency': 'INR', 'payment_capture': '1'})
    return render_template('payment.html', payment=payment, request_id=request_id)

@app.route('/success/<int:request_id>', methods=['POST'])
def success(request_id):
    service_request = ServiceRequest.query.get_or_404(request_id)
    service_request.payment_status = 'completed'
    db.session.commit()
    return render_template('payment_success.html')


@app.route('/mark_completed/<int:request_id>', methods=['POST'])
def mark_completed(request_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    service_request = ServiceRequest.query.get_or_404(request_id)
    if service_request.user_id != session['user_id']:
        return 'Unauthorized', 403

    if service_request.status == 'accepted':
        return redirect(url_for('submit_review', request_id=request_id))

    return 'Invalid request', 400


@app.route('/submit_review/<int:request_id>', methods=['GET', 'POST'])
def submit_review(request_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    service_request = ServiceRequest.query.get_or_404(request_id)
    if service_request.user_id != session['user_id']:
        return 'Unauthorized', 403

    if request.method == 'POST':
        rating = request.form['rating']
        description = request.form['description']

        review = Review(
            user_id=session['user_id'],
            ragpicker_id=service_request.ragpicker_id,
            rating=rating,
            description=description
        )
        db.session.add(review)
        db.session.commit()

        service_request.status = 'completed'
        db.session.commit()

        return redirect(url_for('user_dashboard'))

    return render_template('submit_review.html', service_request=service_request)


@app.route('/ragpicker_reviews')
def ragpicker_reviews():
    if 'ragpicker_id' not in session:
        return redirect(url_for('ragpicker_login'))

    reviews = Review.query.filter_by(ragpicker_id=session['ragpicker_id']).all()
    ragpicker_details = RagpickerDetails.query.filter_by(ragpicker_id=session['ragpicker_id']).first()
    average_rating = db.session.query(db.func.avg(Review.rating)).filter_by(ragpicker_id=session['ragpicker_id']).scalar()

    # Round the average rating to one decimal place
    if average_rating is not None:
        average_rating = round(average_rating, 1)

    return render_template('ragpicker_reviews.html', reviews=reviews, average_rating=average_rating, ragpicker_details=ragpicker_details)



if __name__ == '__main__':
    app.run()
