from flask import Flask, request, render_template, redirect, url_for, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from datetime import datetime
import json

# TODO: 
# - FIX PLAYER SCREEN (RIGHT NOW WHEN CLICKING IT REDIRECTS TO <USERID> INSTEAD OF <USERNAME>)
# - FIX HTML FILES TO DISPLAY DATA AS ROWS


app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://fwsbrmejpihtpr:63694976e4b5c59af5029d3802c625c2ab89828c15f55049f86fe58156f744e9@ec2-34-250-252-161.eu-west-1.compute.amazonaws.com:5432/d3m1dq8b7u0ors'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://hanqiulicai:hanqiulicai@localhost:5434/skelly'


from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
db = SQLAlchemy(app)
migrate = Migrate(app, db)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

def update_total_user_stats(user):

    total_stats = {
        'highScore': 0,
        'totalSkellyDeaths': 0,
        'totalEnemiesKilled': 0,
        'totalDamageDone': 0,
        'totalDamageTaken': 0,
        'totalHeavyAttacksUsed': 0,
        'totalLightAttacksUsed': 0,
        'totalBoomerangsUsed': 0,
        'totalDashesUsed': 0,
        'totalRegularMilkCollected': 0,
        'totalChocolateMilkCollected': 0,
        'totalCoconutMilkCollected': 0,
        'totalDistanceTraveled': 0,
        'totalTimePlayed': 0
    }

    # Get all story runs for user
    story_runs = GameStats.query.filter_by(user_id=user.id).all()
    # get all endless runs for user
    endless_runs = EndlessGameStats.query.filter_by(user_id=user.id).all()

    # Calculate total stats both story and endless
    for run in story_runs:
        total_stats['totalSkellyDeaths'] += run.skellyDeaths
        total_stats['totalEnemiesKilled'] += run.enemiesKilled
        total_stats['totalDamageDone'] += run.damageDone
        total_stats['totalDamageTaken'] += run.damageTaken
        total_stats['totalHeavyAttacksUsed'] += run.heavyAttacksUsed
        total_stats['totalLightAttacksUsed'] += run.lightAttacksUsed
        total_stats['totalBoomerangsUsed'] += run.boomerangsUsed
        total_stats['totalDashesUsed'] += run.dashesUsed
        total_stats['totalRegularMilkCollected'] += run.regularMilkCollected
        total_stats['totalChocolateMilkCollected'] += run.chocolateMilkCollected
        total_stats['totalCoconutMilkCollected'] += run.coconutMilkCollected
        total_stats['totalDistanceTraveled'] += run.distanceTraveled
        total_stats['totalTimePlayed'] += run.timeElapsed
    
    for run in endless_runs:
        total_stats['totalEnemiesKilled'] += run.enemiesKilled
        total_stats['totalDamageDone'] += run.damageDone
        total_stats['totalDamageTaken'] += run.damageTaken
        total_stats['totalHeavyAttacksUsed'] += run.heavyAttacksUsed
        total_stats['totalLightAttacksUsed'] += run.lightAttacksUsed
        total_stats['totalBoomerangsUsed'] += run.boomerangsUsed
        total_stats['totalDashesUsed'] += run.dashesUsed
        total_stats['totalRegularMilkCollected'] += run.regularMilkCollected
        total_stats['totalChocolateMilkCollected'] += run.chocolateMilkCollected
        total_stats['totalCoconutMilkCollected'] += run.coconutMilkCollected
        total_stats['totalDistanceTraveled'] += run.distanceTraveled
        total_stats['totalTimePlayed'] += run.timeElapsed
        total_stats['highScore'] = max(total_stats['highScore'], run.runScore)
    
    # Update the UserStats model with the calculated total stats
    user.highScore = total_stats['highScore']
    user.totalSkellyDeaths = total_stats['totalSkellyDeaths']
    user.totalEnemiesKilled = total_stats['totalEnemiesKilled']
    user.totalDamageDone = total_stats['totalDamageDone']
    user.totalDamageTaken = total_stats['totalDamageTaken']
    user.totalHeavyAttacksUsed = total_stats['totalHeavyAttacksUsed']
    user.totalLightAttacksUsed = total_stats['totalLightAttacksUsed']
    user.totalBoomerangsUsed = total_stats['totalBoomerangsUsed']
    user.totalDashesUsed = total_stats['totalDashesUsed']
    user.totalRegularMilkCollected = total_stats['totalRegularMilkCollected']
    user.totalChocolateMilkCollected = total_stats['totalChocolateMilkCollected']
    user.totalCoconutMilkCollected = total_stats['totalCoconutMilkCollected']
    user.totalDistanceTraveled = total_stats['totalDistanceTraveled']
    user.totalTimePlayed = total_stats['totalTimePlayed']

    # Save the changes to the database
    db.session.commit()

# UserStats Model
class UserStats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #username
    username = db.Column(db.String(50), unique=True)

    # User story stats
    mementosCollected = db.Column(db.Integer, default=0)
    levelReached = db.Column(db.Integer, default=0)
    weaponEquipped = db.Column(db.Integer, default=1)
    skullHammerPickedUpJoe = db.Column(db.Boolean, default=True)
    ribberanPickedUpJane = db.Column(db.Boolean, default=False)
    boneSwordFabulaPickedUp = db.Column(db.Boolean, default=False)
    QuestsCompleted = db.Column(db.Integer, default=0)
    
    # Total stats
    highScore = db.Column(db.Integer, default=0)
    totalSkellyDeaths = db.Column(db.Integer, default=0)
    totalEnemiesKilled = db.Column(db.Integer, default=0)
    totalDamageDone = db.Column(db.Integer, default=0)
    totalDamageTaken = db.Column(db.Integer, default=0)
    totalHeavyAttacksUsed = db.Column(db.Integer, default=0)
    totalLightAttacksUsed = db.Column(db.Integer, default=0)
    totalBoomerangsUsed = db.Column(db.Integer, default=0)
    totalDashesUsed = db.Column(db.Integer, default=0)
    totalRegularMilkCollected = db.Column(db.Integer, default=0)
    totalChocolateMilkCollected = db.Column(db.Integer, default=0)
    totalCoconutMilkCollected = db.Column(db.Integer, default=0)
    totalDistanceTraveled = db.Column(db.Float, default=0.0) 
    totalTimePlayed = db.Column(db.Float, default=0.0) #seconds
    

    # User settings
    cameraSensitivity = db.Column(db.Float, default=0.5) # 0.0 - 1.0
    bgmVolume = db.Column(db.Float, default=0.5) # 0.0 - 1.0
    sfxVolume = db.Column(db.Float, default=0.5) # 0.0 - 1.0
    narrationVolume = db.Column(db.Float, default=0.5) # 0.0 - 1.0
    forwardKey = db.Column(db.String(1), default='w')
    backwardKey = db.Column(db.String(1), default='s')
    leftKey = db.Column(db.String(1), default='a')
    rightKey = db.Column(db.String(1), default='d')
    dashKey = db.Column(db.String(1), default='e')
    lightAttackKey = db.Column(db.String(10), default='space')
    heavyAttackKey = db.Column(db.String(1), default='t')
    powerUpKey = db.Column(db.String(1), default='r')
    forcedPowerUpKey = db.Column(db.String(1), default='g')
    weaponToggleKey = db.Column(db.String(1), default='f')
    textSkipKey = db.Column(db.String(10), default='enter')
    weaponQuickKey1 = db.Column(db.String(1), default='1')
    weaponQuickKey2 = db.Column(db.String(1), default='2')
    weaponQuickKey3 = db.Column(db.String(1), default='3')

    # User runs
    game_stats = db.relationship('GameStats', backref='user', lazy=True)
    endless_game_stats = db.relationship('EndlessGameStats', backref='user', lazy=True)

    def user_story_stats_to_dict(self):
        return {
            'username': self.username,
            'mementosCollected': self.mementosCollected,
            'levelReached': self.levelReached,
            'weaponEquipped': self.weaponEquipped,
            'skullHammerPickedUpJoe': self.skullHammerPickedUpJoe,
            'ribberanPickedUpJane': self.ribberanPickedUpJane,
            'boneSwordFabulaPickedUp': self.boneSwordFabulaPickedUp,
            'QuestsCompleted': self.QuestsCompleted,
        }
    
    def user_total_stats_to_dict(self):
        return {
            'username': self.username,
            'highScore': self.highScore,
            'totalSkellyDeaths': self.totalSkellyDeaths,
            'totalEnemiesKilled': self.totalEnemiesKilled,
            'totalDamageDone': self.totalDamageDone,
            'totalDamageTaken': self.totalDamageTaken,
            'totalHeavyAttacksUsed': self.totalHeavyAttacksUsed,
            'totalLightAttacksUsed': self.totalLightAttacksUsed,
            'totalBoomerangsUsed': self.totalBoomerangsUsed,
            'totalDashesUsed': self.totalDashesUsed,
            'totalRegularMilkCollected': self.totalRegularMilkCollected,
            'totalChocolateMilkCollected': self.totalChocolateMilkCollected,
            'totalCoconutMilkCollected': self.totalCoconutMilkCollected,
            'totalDistanceTraveled': self.totalDistanceTraveled,
            'totalTimePlayed': self.totalTimePlayed,
        }
    
    def user_settings_to_dict(self):
        return {
            'username': self.username,
            'cameraSensitivity': self.cameraSensitivity,
            'bgmVolume': self.bgmVolume,
            'sfxVolume': self.sfxVolume,
            'narrationVolume': self.narrationVolume,
            'forwardKey': self.forwardKey,
            'backwardKey': self.backwardKey,
            'leftKey': self.leftKey,
            'rightKey': self.rightKey,
            'dashKey': self.dashKey,
            'lightAttackKey': self.lightAttackKey,
            'heavyAttackKey': self.heavyAttackKey,
            'forcedPowerUpKey': self.forcedPowerUpKey,
            'powerUpKey': self.powerUpKey,
            'weaponToggleKey': self.weaponToggleKey,
            'textSkipKey': self.textSkipKey,
            'weaponQuickKey1': self.weaponQuickKey1,
            'weaponQuickKey2': self.weaponQuickKey2,
            'weaponQuickKey3': self.weaponQuickKey3,
        }

# GameStats Model
class GameStats(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    username = db.Column(db.String(50), db.ForeignKey('user_stats.username'), nullable=False)
    isGameOver = db.Column(db.Boolean, default=False)

    skellyDeaths = db.Column(db.Integer, default=0)
    enemiesKilled = db.Column(db.Integer, default=0)
    damageDone = db.Column(db.Integer, default=0)
    damageTaken = db.Column(db.Integer, default=0)

    heavyAttacksUsed = db.Column(db.Integer, default=0)
    lightAttacksUsed = db.Column(db.Integer, default=0)
    boomerangsUsed = db.Column(db.Integer, default=0)
    dashesUsed = db.Column(db.Integer, default=0)

    regularMilkCollected = db.Column(db.Integer, default=0)
    chocolateMilkCollected = db.Column(db.Integer, default=0)
    coconutMilkCollected = db.Column(db.Integer, default=0)

    distanceTraveled = db.Column(db.Float, default=0.0)
    timeElapsed = db.Column(db.Float, default=0.0)
    currentLevel = db.Column(db.Integer, default=0)
    playerXPosition = db.Column(db.Float, default=0.0)
    playerYPosition = db.Column(db.Float, default=0.0)
    playerZPosition = db.Column(db.Float, default=0.0)
    healthAtSaveTime = db.Column(db.Integer, default=0)
    

    def to_dict(self):
        return {
            'username': self.username,
            'isGameOver': self.isGameOver,
            'skellyDeaths': self.skellyDeaths,
            'enemiesKilled': self.enemiesKilled,
            'damageDone': self.damageDone,
            'damageTaken': self.damageTaken,
            'heavyAttacksUsed': self.heavyAttacksUsed,
            'lightAttacksUsed': self.lightAttacksUsed,
            'boomerangsUsed': self.boomerangsUsed,
            'dashesUsed': self.dashesUsed,
            'regularMilkCollected': self.regularMilkCollected,
            'chocolateMilkCollected': self.chocolateMilkCollected,
            'coconutMilkCollected': self.coconutMilkCollected,
            'distanceTraveled': self.distanceTraveled,
            'timeElapsed': self.timeElapsed,
            'currentLevel': self.currentLevel,
            'playerXPosition': self.playerXPosition,
            'playerYPosition': self.playerYPosition,
            'playerZPosition': self.playerZPosition,
            'healthAtSaveTime': self.healthAtSaveTime
        }

class EndlessGameStats(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    username = db.Column(db.String(50), db.ForeignKey('user_stats.username'), nullable=False)
    enemiesKilled = db.Column(db.Integer, default=0)
    runScore = db.Column(db.Integer, default=0)
    damageDone = db.Column(db.Integer, default=0)
    damageTaken = db.Column(db.Integer, default=0)
    heavyAttacksUsed = db.Column(db.Integer, default=0)
    lightAttacksUsed = db.Column(db.Integer, default=0)
    boomerangsUsed = db.Column(db.Integer, default=0)
    dashesUsed = db.Column(db.Integer, default=0)
    distanceTraveled = db.Column(db.Float, default=0.0)
    timeElapsed = db.Column(db.Float, default=0.0)
    regularMilkCollected = db.Column(db.Integer, default=0)
    chocolateMilkCollected = db.Column(db.Integer, default=0)
    coconutMilkCollected = db.Column(db.Integer, default=0)

    def to_dict(self):
        return {
            'username': self.username,
            'enemiesKilled': self.enemiesKilled,
            'runScore': self.runScore,
            'damageDone': self.damageDone,
            'damageTaken': self.damageTaken,
            'heavyAttacksUsed': self.heavyAttacksUsed,
            'lightAttacksUsed': self.lightAttacksUsed,
            'boomerangsUsed': self.boomerangsUsed,
            'dashesUsed': self.dashesUsed,
            'distanceTraveled': self.distanceTraveled,
            'timeElapsed': self.timeElapsed,
            'regularMilkCollected': self.regularMilkCollected,
            'chocolateMilkCollected': self.chocolateMilkCollected,
            'coconutMilkCollected': self.coconutMilkCollected
        }

# Endpoints to show data

@app.route('/')
def main_screen():
    return render_template('main_screen.html')

@app.route('/players')
def see_all_players():
    users = UserStats.query.all()
    return render_template('all_players.html', users=users)

@app.route('/players/<username>/story_runs')
def player_story_runs(username):
    user = UserStats.query.filter_by(username=username).first()
    if user:
        runs = GameStats.query.filter_by(username=user.username).all()
        return render_template('player_runs.html', runs=runs, username=username)
    return "User not found", 404

@app.route('/players/<username>/endless_runs')
def player_endless_runs(username):
    user = UserStats.query.filter_by(username=username).first()
    if user:
        runs = EndlessGameStats.query.filter_by(username=user.username).all()
        return render_template('player_endless_runs.html', runs=runs, username=username)
    return "User not found", 404

@app.route('/all_story_runs')
def retrieve_all_story_runs():
    runs = GameStats.query.all()
    return render_template('all_story_runs.html', runs=runs)

@app.route('/all_endless_runs')
def retrieve_all_endless_runs():
    runs = EndlessGameStats.query.all()
    return render_template('all_endless_runs.html', runs=runs)


# Endpoints to add / get data

# endpoint to get the latest story run for a user (save system)
@app.route('/unity/user/<username>/latest_story_run')
def latest_run(username):
    user = UserStats.query.filter_by(username=username).first()
    if user:
        latest_story_run = GameStats.query.filter_by(username=username, isGameOver=False).order_by(GameStats.timestamp.desc()).first()
        if latest_story_run:
            return jsonify(latest_story_run.to_dict())
        else:
            return jsonify({'error': 'No story runs found for player'}), 404
    return jsonify({'error': 'User not found'}), 404

# endpoint to save a new story run, called at the end of each level or when the user quits midpoint
@app.route('/unity/save_story_run', methods=['POST'])
def save_story_run():
    data = request.json
    user = UserStats.query.filter_by(username=data['username']).first()
    if user:
        new_run = GameStats(
            username=data['username'],
            isGameOver=data['isGameOver'],
            skellyDeaths=data['skellyDeaths'],
            enemiesKilled=data['enemiesKilled'],
            damageDone=data['damageDone'],
            damageTaken=data['damageTaken'],
            heavyAttacksUsed=data['heavyAttacksUsed'],
            lightAttacksUsed=data['lightAttacksUsed'],
            boomerangsUsed=data['boomerangsUsed'],
            dashesUsed=data['dashesUsed'],
            regularMilkCollected=data['regularMilkCollected'],
            chocolateMilkCollected=data['chocolateMilkCollected'],
            coconutMilkCollected=data['coconutMilkCollected'],
            distanceTraveled=data['distanceTraveled'],
            timeElapsed=data['timeElapsed'],
            currentLevel=data['currentLevel'],
            playerXPosition=data['playerXPosition'],
            playerYPosition=data['playerYPosition'],
            playerZPosition=data['playerZPosition'],
            healthAtSaveTime=data['healthAtSaveTime']
        )
        db.session.add(new_run)
        db.session.commit()
        return jsonify({'message': 'Run saved successfully', 'id': new_run.id}), 201
    else:
        return jsonify({'error': 'User not found'}), 333
    
# endpoint to save an endless run, called when player dies (if quits, doesnt save)
@app.route('/unity/save_endless_run', methods=['POST'])
def save_endless_run():
    data = request.json
    user = UserStats.query.filter_by(username=data['username']).first()
    if user:
        new_run = EndlessGameStats(
            username=data['username'],
            enemiesKilled=data['enemiesKilled'],
            runScore=data['runScore'],
            damageDone=data['damageDone'],
            damageTaken=data['damageTaken'],
            heavyAttacksUsed=data['heavyAttacksUsed'],
            lightAttacksUsed=data['lightAttacksUsed'],
            boomerangsUsed=data['boomerangsUsed'],
            dashesUsed=data['dashesUsed'],
            regularMilkCollected=data['regularMilkCollected'],
            chocolateMilkCollected=data['chocolateMilkCollected'],
            coconutMilkCollected=data['coconutMilkCollected'],
            distanceTraveled=data['distanceTraveled'],
            timeElapsed=data['timeElapsed']
        )
        db.session.add(new_run)
        db.session.commit()
        return jsonify({'message': 'Run saved successfully', 'id': new_run.id}), 201
    else:
        return jsonify({'error': 'User not found'}), 404

@app.route('/unity/user/<username>/story_stats', methods=['GET'])
def get_user_story_stats(username):
    # Check if the user exists
    user = UserStats.query.filter_by(username=username).first()
    if not user:
        # If user does not exist, create a new user with default values
        user = UserStats(username=username)
        db.session.add(user)
        db.session.commit()
    # Retrieve and return user statistics
    user_stats = user.user_story_stats_to_dict()
    return jsonify({'user_stats': user_stats}), 200

@app.route('/unity/user/<username>/total_stats', methods=['GET'])
def get_total_user_stats(username):
    # Fetch the user from the database
    user = UserStats.query.filter_by(username=username).first()
    # Check if the user exists
    if not user:
        return jsonify({'error': 'User not found'}), 404
    # Calculate the total stats for the user
    update_total_user_stats(user)

    user_stats = user.user_total_stats_to_dict()
    # Return the total stats in the response
    return jsonify({'user_stats': user_stats}), 200


@app.route('/unity/user/<username>/settings', methods=['GET'])
def get_user_settings(username):
    # Check if the user exists
    user = UserStats.query.filter_by(username=username).first()

    if not user:
        # If user does not exist, create a new user with default values
        user = UserStats(username=username)
        db.session.add(user)
        db.session.commit()

    # Retrieve and return user settings
    user_settings = user.user_settings_to_dict()
    return jsonify({'user_settings': user_settings}), 200

# endpoint to update user_story_stats, called after each run
@app.route('/unity/update_user_story_stats', methods=['PUT'])
def update_user_story_stats():
    data = request.json
    user = UserStats.query.filter_by(username=data['username']).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Update user persistent story data
    user.mementosCollected = data['mementosCollected']
    user.levelReached = max(data['levelReached'], user.levelReached)  # Update to the higher level
    user.weaponEquipped = data['weaponEquipped']
    user.skullHammerPickedUpJoe = data['skullHammerPickedUpJoe']
    user.ribberanPickedUpJane = data['ribberanPickedUpJane']
    user.boneSwordFabulaPickedUp = data['boneSwordFabulaPickedUp']
    user.QuestsCompleted = data['QuestsCompleted']
    
    db.session.commit()
    return jsonify({'message': 'User stats updated successfully', 'username': user.username}), 200

@app.route('/unity/update_user_settings', methods=['PUT'])
def update_user_settings():
    data = request.json
    user = UserStats.query.filter_by(username=data['username']).first()

    if not user:
        return jsonify({'error': 'User not found'}), 404

    user.cameraSensitivity = data['cameraSensitivity']
    user.bgmVolume = data['bgmVolume']
    user.sfxVolume = data['sfxVolume']
    user.narrationVolume = data['narrationVolume']
    user.forwardKey = data['forwardKey']
    user.backwardKey = data['backwardKey']
    user.leftKey = data['leftKey']
    user.rightKey = data['rightKey']
    user.dashKey = data['dashKey']
    user.lightAttackKey = data['lightAttackKey']
    user.heavyAttackKey = data['heavyAttackKey']
    user.powerUpKey = data['powerUpKey']
    user.forcedPowerUpKey = data['forcedPowerUpKey']
    user.weaponToggleKey = data['weaponToggleKey']
    user.textSkipKey = data['textSkipKey']
    user.weaponQuickKey1 = data['weaponQuickKey1']
    user.weaponQuickKey2 = data['weaponQuickKey2']
    user.weaponQuickKey3 = data['weaponQuickKey3']

    db.session.commit()
    return jsonify({'message': 'User settings updated successfully', 'username': user.username}), 200


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)