from flask import Flask, request, render_template, redirect, url_for, jsonify
from flask_migrate import Migrate
from datetime import timedelta
import json

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://fwsbrmejpihtpr:63694976e4b5c59af5029d3802c625c2ab89828c15f55049f86fe58156f744e9@ec2-34-250-252-161.eu-west-1.compute.amazonaws.com:5432/d3m1dq8b7u0ors'

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Player(db.Model):
    player_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    date_joined = db.Column(db.DateTime, default=db.func.current_timestamp())
    time_played = db.Column(db.Interval, default=timedelta(0))

class Highscore(db.Model):
    score_id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('player.player_id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    date_achieved = db.Column(db.DateTime, default=db.func.current_timestamp())

class NumberEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<NumberEntry {self.number}>'

#### FRONTEND ROUTES ####

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/add_player', methods=['GET', 'POST'])
def add_player():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        new_player = Player(username=username, email=email)
        db.session.add(new_player)
        db.session.commit()
        return redirect(url_for('add_player'))
    return render_template('add_player.html')

@app.route('/all_players', methods=['GET', 'POST'])
def all_players():
    players = Player.query.all()
    return render_template('all_players.html', players=players)

@app.route('/time_played', methods=['GET', 'POST'])
def time_played():
    players = Player.query.all()
    return render_template('players_time_played.html', players=players)

@app.route('/submit_score', methods=['GET', 'POST'])
def submit_score():
    if request.method == 'POST':
        player_id = request.form['player_id']
        score = request.form['score']
        new_score = Highscore(player_id=player_id, score=score)
        db.session.add(new_score)
        db.session.commit()
        return redirect(url_for('submit_score'))
    players = Player.query.all()
    return render_template('submit_score.html', players=players)

@app.route('/highscores')
def highscores():
    scores = Highscore.query.order_by(Highscore.score.desc()).all()
    return render_template('highscores.html', scores=scores)

@app.route('/view_numbers')
def view_numbers():
    numbers = NumberEntry.query.all()
    return render_template('view_numbers.html', numbers=numbers)


#### ROUTES TO ADD / READ STUFF TO THE DATABASE ####

# Route to add a new player (POST) and retrieve all players (GET)
@app.route('/add_player_json', methods=['GET', 'POST'])
def add_player_json():
    """
    Add a new player to the database (POST) if the username doesn't exist, or
    retrieve all players (GET).

    Expected JSON format for POST:
    {
        "username": "user123"
    }

    Response JSON format for POST:
    If the username doesn't exist:
    {
        "message": "Player added successfully"
    }
    If the username already exists:
    {
        "error": "Username already exists"
    }

    Response JSON format for GET:
    [
        {
            "player_id": 1,
            "username": "user123"
        },
        {
            "player_id": 2,
            "username": "another_user"
        },
        # ... (more players)
    ]
    """
    if request.method == 'POST':
        data = request.json
        username = data.get('username', '').strip()
        
        # Check if the username already exists
        existing_player = Player.query.filter_by(username=username).first()
        if existing_player:
            return jsonify({"error": "Username already exists"}), 400
        
        new_player = Player(username=username)
        db.session.add(new_player)
        db.session.commit()
        return jsonify({"message": "Player added successfully"}), 201
    elif request.method == 'GET':
        players = Player.query.all()
        player_list = [
            {
                "player_id": player.player_id,
                "username": player.username
            }
            for player in players
        ]
        return jsonify(player_list)

# Route to submit a score (POST) and retrieve all scores (GET)
@app.route('/submit_score_json', methods=['GET', 'POST'])
def submit_score_json():
    """
    Submit a player's score (POST) or retrieve all scores (GET).

    Expected JSON format for POST:
    {
        "player_id": 1,
        "score": 100
    }

    Response JSON format for POST:
    {
        "message": "Score submitted successfully"
    }

    Response JSON format for GET:
    [
        {
            "score_id": 1,
            "player_id": 1,
            "score": 100
        },
        {
            "score_id": 2,
            "player_id": 2,
            "score": 150
        },
        # ... (more scores)
    ]
    """
    if request.method == 'POST':
        data = request.json
        player_id = data.get('player_id', None)
        score = data.get('score', None)

        # Check if player_id is provided and exists
        if player_id is None or Player.query.get(player_id) is None:
            return jsonify({"error": "Invalid player_id"}), 400

        # Check if score is provided
        if score is None:
            return jsonify({"error": "Score is required"}), 400

        new_score = Highscore(player_id=player_id, score=score)
        db.session.add(new_score)
        db.session.commit()
        return jsonify({"message": "Score submitted successfully"}), 201
    elif request.method == 'GET':
        scores = Highscore.query.all()
        score_list = [
            {
                "score_id": score.score_id,
                "player_id": score.player_id,
                "score": score.score
            }
            for score in scores
        ]
        return jsonify(score_list)

# Route to update time played (POST) and retrieve all players with time played (GET)
@app.route('/update_time_played_json', methods=['GET', 'POST'])
def update_time_played_json():
    """
    Update a player's time played (POST) or retrieve all players with time played (GET).

    Expected JSON format for POST:
    {
        "player_id": 1,
        "time_played": 3600
    }

    Response JSON format for POST:
    {
        "message": "Time updated successfully"
    }

    Response JSON format for GET:
    [
        {
            "player_id": 1,
            "username": "user123",
            "time_played": 3600.0
        },
        {
            "player_id": 2,
            "username": "another_user",
            "time_played": 7200.0
        },
        # ... (more players with time played)
    ]
    """
    if request.method == 'POST':
        data = request.json
        player_id = data.get('player_id', None)
        time_played = data.get('time_played', None)

        # Check if player_id is provided and exists
        if player_id is None or Player.query.get(player_id) is None:
            return jsonify({"error": "Invalid player_id"}), 400

        # Check if time_played is provided
        if time_played is None:
            return jsonify({"error": "Time played is required"}), 400

        player = Player.query.get(player_id)
        if player:
            player.time_played += timedelta(seconds=time_played)
            db.session.commit()
            return jsonify({"message": "Time updated successfully"}), 200
        return jsonify({"error": "Player not found"}), 404
    elif request.method == 'GET':
        players = Player.query.all()
        player_list = [
            {
                "player_id": player.player_id,
                "username": player.username,
                "time_played": player.time_played.total_seconds()
            }
            for player in players
        ]
        return jsonify(player_list)

# Route to submit a number (POST) and retrieve all numbers (GET)
@app.route('/submit_number_json', methods=['GET', 'POST'])
def submit_number_json():
    """
    Submit a number (POST) or retrieve all numbers (GET).

    Expected JSON format for POST:
    {
        "number": 42
    }

    Response JSON format for POST:
    {
        "message": "Number added successfully"
    }

    Response JSON format for GET:
    [
        {
            "id": 1,
            "number": 42
        },
        {
            "id": 2,
            "number": 123
        },
        # ... (more numbers)
    ]
    """
    if request.method == 'POST':
        try:
            data = request.json
            new_number = NumberEntry(number=data['number'])
            db.session.add(new_number)
            db.session.commit()
            return {"message": "Number added successfully"}, 200
        except KeyError as e:
            return {"error": f"Missing key: {e}"}, 400
    elif request.method == 'GET':
        numbers = NumberEntry.query.all()
        number_list = [
            {
                "id": number.id,
                "number": number.number
            }
            for number in numbers
        ]
        return jsonify(number_list)

# Add other routes as needed...

if __name__ == '__main__':
    app.run(debug=True)