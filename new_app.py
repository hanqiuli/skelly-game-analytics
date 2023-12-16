from flask import Flask, request, render_template, redirect, url_for, jsonify
from flask_migrate import Migrate
from datetime import datetime
import json

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://fwsbrmejpihtpr:63694976e4b5c59af5029d3802c625c2ab89828c15f55049f86fe58156f744e9@ec2-34-250-252-161.eu-west-1.compute.amazonaws.com:5432/d3m1dq8b7u0ors'

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)
migrate = Migrate(app, db)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
class GameStats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.JSON)  # Stores the JSON data of game stats
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'data': self.data,
            'timestamp': self.timestamp.isoformat()
        }

@app.route('/save_game_data', methods=['POST'])
def save_game_data():
    data = request.json
    new_stats = GameStats(data=data)
    db.session.add(new_stats)
    db.session.commit()
    return jsonify({'message': 'Game data saved successfully', 'id': new_stats.id}), 201

@app.route('/load_game_data', methods=['GET'])
def load_game_data():
    latest_stats = GameStats.query.order_by(GameStats.timestamp.desc()).first()
    if latest_stats:
        return jsonify(latest_stats.to_dict())
    else:
        return jsonify({'error': 'No game data found'}), 404

@app.route('/view_data')
def view_data():
    game_stats = GameStats.query.order_by(GameStats.timestamp.desc()).all()
    return render_template('view_data.html', game_stats=game_stats)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)