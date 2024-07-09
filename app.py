from flask import Flask, render_template, request,redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://default:SA57KMxEhzwb@ep-holy-firefly-a1hm97ya.ap-southeast-1.aws.neon.tech:5432/verceldb?sslmode=require"
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#
# db = SQLAlchemy(app)
#
# class User(db.Model):
#     __tablename__ = 'login'
#
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(50), unique=True, nullable=False)
#     password = db.Column(db.String(100), nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#
#         username = request.form['username']
#         password = request.form['password']
#
#         if User.query.filter_by(username=username).first():
#             return 'Username is already taken!'
#
#         new_user = User(username=username, password=password)
#
#         db.session.add(new_user)
#
#         db.session.commit()
#
#         return redirect(url_for('login'))
#
#     return render_template('register.html')
#
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#
#         user = User.query.filter_by(username=username).first()
#
#         if user and user.password == password:
#             session['user_id'] = user.id
#             return redirect(url_for('dashboard'))
#         else:
#             return 'Invalid username or password. Please try again.'
#
#     return render_template('login.html')

if __name__ == '__main__':
    with app.app_context():
    #db.create_all()
    app.run()
