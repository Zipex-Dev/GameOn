from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)

# Create the User model for the database
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

# Create the Game model for the database (optional, depending on your needs)
class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    location = db.Column(db.String(150), nullable=False)
    date_time = db.Column(db.String(50), nullable=False)
    available_spots = db.Column(db.Integer, nullable=False)

# Initialize the database
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/games')
def games():
    game_list = [
        {'name': 'Basketball Game', 'location': 'Sports Field 1', 'date_time': '2025-03-25 16:00', 'available_spots': 5},
        {'name': 'Soccer Match', 'location': 'Indoor Arena 3', 'date_time': '2025-03-26 18:00', 'available_spots': 8}
    ]
    return render_template('games.html', games=game_list)

@app.route('/create-game')
def create_game():
    return render_template('create_game.html')

@app.route('/submit-game', methods=['POST'])
def submit_game():
    game_name = request.form['gameName']
    location = request.form['location']
    date_time = request.form['dateTime']
    available_spots = request.form['availableSpots']
    game_type = request.form['gameType']
    additional_notes = request.form['additionalNotes']
    
    # Here you can save the data to the database or do further processing
    new_game = Game(name=game_name, location=location, date_time=date_time, available_spots=available_spots)
    db.session.add(new_game)
    db.session.commit()
    
    flash("Game created successfully!", "success")
    return redirect(url_for('games'))

@app.route('/create-account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Check if passwords match
        if password != confirm_password:
            flash('Passwords do not match!', 'danger')
            return redirect(url_for('create_account'))

        # Hash the password before storing it
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')


        # Create a new user and add to the database
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('create_account.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password, password):
            flash('Logged in successfully!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials, please try again.', 'danger')
    
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
