from mainapp import app
from mainapp.api.models import *
from flask import request, session, jsonify
from copy import deepcopy
import json
import hashlib
import simulate_fight


# Routes
@app.route("/")
def hello():
    if app.debug:
        return "<h1>Warning : DEBUG mode</h1>Welcome to our serious game server"
    else:
        return "Welcome to our serious game server<br/><i>Running as production server</i>"

@app.route("/api/signup", methods=['POST'])
def route_signup():
    name = request.form['name']
    password = request.form['password']

    print Player.query.filter_by(name=name).first()

    existing_player = Player.query.filter_by(name=name).first()
    if existing_player != None:
        return buildErrorResponse('User already exists')

    player = Player(name, password)
    db.session.add(player)
    db.session.commit()

    return buildSuccessResponse({'id': player.id})

@app.route("/api/test", methods=['POST'])
def route_test():
    data = dict((key, request.form.getlist(key)) for key in request.form.keys())
    return json.dumps(data)

@app.route("/api/signin", methods=['POST'])
def route_signin():
    name = request.form['name']
    password = request.form['password']

    m = hashlib.md5()
    m.update(password)
    password_hashed = m.hexdigest()

    existing_player = Player.query.filter_by(name=name, password=password_hashed).first()

    if existing_player == None:
        return buildErrorResponse('Bad password or username')

    id = existing_player.id
    print "Signing in of", id
    session['user_id'] = id

    return buildSuccessResponse({'id': id})

@app.route("/api/ia/save", methods=['POST'])
def route_ia_save():
    if 'user_id' in session:
        current_player = Player.query.filter_by(id=session['user_id']).first()

        if current_player == None:
            return buildErrorResponse('Unknown error')

        current_player.iaCode = request.form['code']
        
        db.session.commit()

        return buildSuccessResponse()
    else:
        return buildErrorResponse('Not signed in')

@app.route("/api/ia/get")
def route_ia_get():
    if 'user_id' in session:
        current_player = Player.query.filter_by(id=session['user_id']).first()

        if current_player == None:
            return buildErrorResponse('Unknown error')

        return buildSuccessResponse({'code': current_player.iaCode})
    else:
        print 'Not signed in !'
        return buildErrorResponse('Not signed in')

@app.route("/api/ia/run")
def route_ia_run():
    return buildErrorResponse('Not implemented yet')

@app.route("/api/logout", methods=['GET'])
def route_logout():
    session.pop('user_id', None)
    return buildSuccessResponse()

@app.route("/api/user/id", methods=['GET'])
def route_user_id():
    if 'user_id' in session:
        return buildSuccessResponse({'id': session['user_id']})
    else:
        return buildErrorResponse('Not signed in')

@app.route("/api/users/list", methods=['GET'])
def route_users_list():
    print Player.query.order_by(Player.name)
    all_players = Player.query.order_by(Player.name)
    print all_players[0].serialize()
    return buildSuccessResponse({'players': [i.serialize() for i in all_players]})

@app.route("/api/fight/launch", methods=['POST'])
def route_gifht_launch():
    askingFightPlayer = Player.query.filter_by(id=session['user_id']).first()
    fightedPlayer = Player.query.filter_by(id=request.form['enemyId']).first()
    print askingFightPlayer, 'fighting against ', fightedPlayer
    fight_result = simulate_fight.emulate(askingFightPlayer.iaCode, fightedPlayer.iaCode)
    
    return buildSuccessResponse({'fightResult': fight_result})


def buildErrorResponse(info = 'Unknown issue', responseDict= None):
    if not responseDict:
        responseDict = {}

    responseDict['info'] = info

    responseDict['response'] = 'fail'
    return json.dumps(responseDict)

def buildSuccessResponse(responseDict= None):
    if not responseDict:
        responseDict = {}

    responseDict['response'] = 'success'
    return json.dumps(responseDict)
