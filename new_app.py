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
class GameStats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    isGameOver = db.Column(db.Boolean, default=False)
    skellyDeaths = db.Column(db.Integer, default=0)
    enemiesKilled = db.Column(db.Integer, default=0)
    damageDone = db.Column(db.Integer, default=0)
    damageTaken = db.Column(db.Integer, default=0)
    heavyAttacksUsed = db.Column(db.Integer, default=0)
    lightAttacksUsed = db.Column(db.Integer, default=0)
    dashesUsed = db.Column(db.Integer, default=0)
    distanceTraveled = db.Column(db.Float, default=0.0)
    timeElapsed = db.Column(db.Float, default=0.0)
    mementosCollected = db.Column(db.Integer, default=0)
    levelReached = db.Column(db.Integer, default=0)
    upgradesMilkCollected = db.Column(db.Integer, default=0)
    skullHammerPickedUpJoe = db.Column(db.Boolean, default=False)
    ribberanPickedUpJane = db.Column(db.Boolean, default=False)
    boneSwordFabulaPickedUp = db.Column(db.Boolean, default=False)
    weaponEquipped = db.Column(db.Integer, default=1)
    currentLevel = db.Column(db.Integer, default=0)
    playerXPosition = db.Column(db.Float, default=0.0)
    playerYPosition = db.Column(db.Float, default=0.0)
    playerZPosition = db.Column(db.Float, default=0.0)
    healthAtSaveTime = db.Column(db.Integer, default=0)

    def to_dict(self):
        return {
            'id': self.id,
            'isGameOver': self.isGameOver,
            'skellyDeaths': self.skellyDeaths,
            'enemiesKilled': self.enemiesKilled,
            'damageDone': self.damageDone,
            'damageTaken': self.damageTaken,
            'heavyAttacksUsed': self.heavyAttacksUsed,
            'lightAttacksUsed': self.lightAttacksUsed,
            'dashesUsed': self.dashesUsed,
            'distanceTraveled': self.distanceTraveled,
            'timeElapsed': self.timeElapsed,
            'mementosCollected': self.mementosCollected,
            'levelReached': self.levelReached,
            'upgradesMilkCollected': self.upgradesMilkCollected,
            'skullHammerPickedUpJoe': self.skullHammerPickedUpJoe,
            'ribberanPickedUpJane': self.ribberanPickedUpJane,
            'boneSwordFabulaPickedUp': self.boneSwordFabulaPickedUp,
            'weaponEquipped': self.weaponEquipped,
            'currentLevel': self.currentLevel,
            'playerXPosition': self.playerXPosition,
            'playerYPosition': self.playerYPosition,
            'playerZPosition': self.playerZPosition,
            'healthAtSaveTime': self.healthAtSaveTime,
            'timestamp': self.timestamp.isoformat()
        }

@app.route('/save_game_data', methods=['POST'])
def save_game_data():
    data = request.json
    new_stats = GameStats(
        isGameOver=data.get('isGameOver', False),
        skellyDeaths=data.get('skellyDeaths', 0),
        enemiesKilled=data.get('enemiesKilled', 0),
        damageDone=data.get('damageDone', 0),
        damageTaken=data.get('damageTaken', 0),
        heavyAttacksUsed=data.get('heavyAttacksUsed', 0),
        lightAttacksUsed=data.get('lightAttacksUsed', 0),
        dashesUsed=data.get('dashesUsed', 0),
        distanceTraveled=data.get('distanceTraveled', 0.0),
        timeElapsed=data.get('timeElapsed', 0.0),
        mementosCollected=data.get('mementosCollected', 0),
        levelReached=data.get('levelReached', 0),
        upgradesMilkCollected=data.get('upgradesMilkCollected', 0),
        skullHammerPickedUpJoe=data.get('skullHammerPickedUpJoe', False),
        ribberanPickedUpJane=data.get('ribberanPickedUpJane', False),
        boneSwordFabulaPickedUp=data.get('boneSwordFabulaPickedUp', False),
        weaponEquipped=data.get('weaponEquipped', 1),
        currentLevel=data.get('currentLevel', 0),
        playerXPosition=data.get('playerXPosition', 0.0),
        playerYPosition=data.get('playerYPosition', 0.0),
        playerZPosition=data.get('playerZPosition', 0.0),
        healthAtSaveTime=data.get('healthAtSaveTime', 0)
    )
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
    app.run(debug=True)