from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_user, current_user, login_required, logout_user, UserMixin, AnonymousUserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'Software-Samurai'

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(80), unique=True, nullable=False)
    lastname = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    mobile = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    def is_active(self):
        return True

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/api/data', methods=['GET', 'POST'])
def api_data():
    if request.method == 'GET':
        # Handle GET request logic
        # For example, you can retrieve data from the database or perform any other operations
        # Return the data in the desired format (e.g., JSON)
        data = {
            'message': 'GET request successful',
            'data': 'Sample data',
        }
        return jsonify(data)

    elif request.method == 'POST':
        data = request.get_json()
        # Handle POST request logic
        # Process the received data, save it to the database, or perform any other operations
        # Return a response indicating the success of the operation or any relevant data
        response_data = {
            'message': 'POST request successful',
            'data': data,
        }
        return jsonify(response_data)

@app.route('/')
@login_required
def index():
    message = "Welcome!"
    if not isinstance(current_user._get_current_object(), AnonymousUserMixin):
        message = "Welcome, " + current_user.username + "!"
    return render_template('index.html', message=message)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        mobile = request.form['mobile']
        password = generate_password_hash(request.form['password'], method='sha256')

        # Check if user already exists
        if User.query.filter_by(email=email).first():
            flash('Email address already exists')
            return redirect(url_for('register'))

        user = User(firstname=firstname, lastname=lastname, email=email, mobile=mobile, password=password)
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))

        flash('Invalid email or password')

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


if __name__ == '__main__':
    from flask_cors import CORS
    CORS(app)
    with app.app_context():
        db.create_all()
    app.run(port=8000, debug=True)