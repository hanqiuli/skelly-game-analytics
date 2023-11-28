from flask import Flask, request, render_template, redirect, url_for
app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/game_data'
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://fwsbrmejpihtpr:63694976e4b5c59af5029d3802c625c2ab89828c15f55049f86fe58156f744e9@ec2-34-250-252-161.eu-west-1.compute.amazonaws.com:5432/d3m1dq8b7u0ors"

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)

class Player(db.Model):
    player_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    date_joined = db.Column(db.DateTime, default=db.func.current_timestamp())

class Highscore(db.Model):
    score_id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('player.player_id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    date_achieved = db.Column(db.DateTime, default=db.func.current_timestamp())

# Create the tables
with app.app_context():
    db.create_all()

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

if __name__ == '__main__':
    app.run(debug=True)