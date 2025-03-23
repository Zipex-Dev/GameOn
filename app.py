from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = 'rafa2112'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

# Game model
class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    location = db.Column(db.String(150), nullable=False)
    date_time = db.Column(db.String(50), nullable=False)
    available_spots = db.Column(db.Integer, nullable=False)
    game_type = db.Column(db.String(50), nullable=False)  # Ensure this column exists
    additional_notes = db.Column(db.Text, nullable=True)

# JoinRequest model
class JoinRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # User requesting to join
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)  # Game they want to join
    status = db.Column(db.String(50), nullable=False, default="pending")  # Request status (e.g., pending, approved)

    user = db.relationship('User', backref=db.backref('join_requests', lazy=True))
    game = db.relationship('Game', backref=db.backref('join_requests', lazy=True))


# Initialize the database
with app.app_context():
    db.create_all()

# Home page (redirect to login if not logged in)
@app.route('/')
def index():
    if 'user_id' not in session:  # If the user is not logged in, redirect to login
        return redirect(url_for('login'))
    return render_template('index.html')

# Create game page (render create game form)
@app.route('/create-game')
def create_game():
    return render_template('create_game.html')

# Submit game data to the database
@app.route('/submit-game', methods=['POST'])
def submit_game():
    if 'user_id' not in session:
        return redirect(url_for('login'))  # Redirect to login if not logged in
    
    # Get the data from the form
    game_name = request.form['gameName']
    location = request.form['location']
    date_time = request.form['dateTime']
    available_spots = request.form['availableSpots']
    game_type = request.form['gameType']
    additional_notes = request.form['additionalNotes']
    
    # Create a new game and add to the database
    new_game = Game(
        name=game_name,
        location=location,
        date_time=date_time,
        available_spots=available_spots,
        game_type=game_type,
        additional_notes=additional_notes
    )
    db.session.add(new_game)
    db.session.commit()
    
    flash("Game created successfully!", "success")
    return redirect(url_for('games'))

# Games page (view available games)
@app.route('/games')
def games():
    game_list = Game.query.all()  # Get all games from the database
    return render_template('games.html', games=game_list)

# Account creation route (for new users)
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

# Login route (for existing users)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id  # Store user ID in session
            flash('Logged in successfully!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials, please try again.', 'danger')
    
    return render_template('login.html')

# Logout route (clear session and redirect to home page)
@app.route('/logout')
def logout():
    session.pop('user_id', None)  # Remove user from session
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))

# Profile page route (only accessible when logged in)
@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))  # Redirect to login if not logged in
    
    user = User.query.get(session['user_id'])  # Get the logged-in user from the database
    return render_template('profile.html', user=user)

# Join game route (for public games)
@app.route('/join-game/<int:game_id>', methods=['POST'])
def join_game(game_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))  # Redirect to login if not logged in
    
    game = Game.query.get(game_id)
    if game and game.game_type == 'public':
        # Directly join the public game
        flash("You have joined the game!", "success")
        return redirect(url_for('games'))
    else:
        flash("This game is private. Please send a join request.", "warning")
        return redirect(url_for('games'))

# Join request route (for private games)
@app.route('/request-join/<int:game_id>', methods=['POST'])
def request_join(game_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))  # Redirect to login if not logged in

    game = Game.query.get(game_id)
    if game and game.game_type == 'private':
        user_id = session['user_id']
        join_request = JoinRequest(user_id=user_id, game_id=game.id)
        db.session.add(join_request)
        db.session.commit()
        flash("Your request to join the game has been sent!", "success")
        return redirect(url_for('games'))
    else:
        flash("This game doesn't exist or is not private.", "danger")
        return redirect(url_for('games'))

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
