from flask import Flask, request, render_template, redirect, url_for, jsonify
from datetime import timedelta
import json

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/game_data'
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)

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

@app.route('/time_played')
def time_played():
    players = Player.query.all()
    return render_template('time_played.html', players=players)

@app.route('/view_numbers')
def view_numbers():
    numbers = NumberEntry.query.all()
    return render_template('view_numbers.html', numbers=numbers)


#### ROUTES TO ADD STUFF TO THE DATABASE ####

# Route to add a new player
# URL https://skelly-game-analytics-bab21bc24913.herokuapp.com/add_player_json
# Expected JSON format: {"username": "user123", "email": "email@example.com"}
@app.route('/add_player_json', methods=['POST'])
def add_player_json():
    data = request.json
    new_player = Player(username=data['username'], email=data['email'])
    db.session.add(new_player)
    db.session.commit()
    return jsonify({"message": "Player added successfully"}), 201

# Route to submit a score
# URL https://skelly-game-analytics-bab21bc24913.herokuapp.com/submit_score_json
# Expected JSON format: {"player_id": 1, "score": 100}
@app.route('/submit_score_json', methods=['POST'])
def submit_score_json():
    data = request.json
    new_score = Highscore(player_id=data['player_id'], score=data['score'])
    db.session.add(new_score)
    db.session.commit()
    return jsonify({"message": "Score submitted successfully"}), 201

# Route to update time played
# URL https://skelly-game-analytics-bab21bc24913.herokuapp.com/update_time_played_json
# Expected JSON format: {"player_id": 1, "time_played": 3600}
@app.route('/update_time_played_json', methods=['POST'])
def update_time_played_json():
    data = request.json
    player = Player.query.get(data['player_id'])
    if player:
        player.time_played += timedelta(seconds=data['time_played'])
        db.session.commit()
        return jsonify({"message": "Time updated successfully"}), 200
    return jsonify({"error": "Player not found"}), 404

@app.route('/submit_number', methods=['POST'])
def submit_number():
    data = request.get_json()
    new_number = NumberEntry(number=data['number'])
    db.session.add(new_number)
    db.session.commit()
    return {"message": "Number added successfully"}, 200

# Add other routes as needed...

if __name__ == '__main__':
    app.run(debug=True)