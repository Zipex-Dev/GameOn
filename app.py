from flask import Flask, render_template, request

app = Flask(__name__)

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
    print(f"Game Created: {game_name}, {location}, {date_time}, {available_spots} spots")
    
    # Redirect or show a success message
    return render_template('index.html', message="Game created successfully!")

if __name__ == '__main__':
    app.run(debug=True)
