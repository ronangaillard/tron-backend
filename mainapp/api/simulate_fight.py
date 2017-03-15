import lupa
from lupa import LuaRuntime
import json
import sys

GAME_SIZE = 20

PLAYER_1_INITIAL_X = 0
PLAYER_1_INITIAL_Y = 10
PLAYER_2_INITIAL_X = GAME_SIZE
PLAYER_2_INITIAL_Y = 10

NUMBER_OF_PLAYERS = 2

PLAYERS_INIT_DIR = ['E', 'W', 'N', 'S']
PLAYERS_INIT_POS = [    [0, 10],
                        [GAME_SIZE, 10]]

class InterpretationError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)



def emulate(player1_code, player2_code):
    print 'running'
    lua = LuaRuntime(unpack_returned_tuples=True) 
    print "Getting player 1 code"
    try:
        print 'code 1 : ', 'function (walls, pos_x, pos_y, direction)\n' + player1_code + '\nend'
        lua_func_player_1 = lua.eval('function (walls, pos_x, pos_y, direction)\n' + player1_code + '\nend')
    except Exception as ex:
        print 'error'
        raise InterpretationError('Syntax error in your code. '+ ex.message)

    try:
        print 'code 2 : ', 'function (walls, pos_x, pos_y, direction)\n' + player2_code + '\nend'
        lua_func_player_2 = lua.eval('function (walls, pos_x, pos_y, direction)\n' + player2_code + '\nend')
    except:
        print 'error'
        raise InterpretationError('Syntax error in enemy\'s code. Fight someone else :/')

    players = []

    for i in range(NUMBER_OF_PLAYERS):
        print 'Creating player with index', i

        players.append({})

        players[i]['dir'] = PLAYERS_INIT_DIR[i]

        players[i]['x'] = PLAYERS_INIT_POS[i][0]
        players[i]['y'] = PLAYERS_INIT_POS[i][1]

        players[i]['initial_x'] = PLAYERS_INIT_POS[i][0]
        players[i]['initial_y'] = PLAYERS_INIT_POS[i][1]

        players[i]['initialPosition'] = [ PLAYERS_INIT_POS[i][0], PLAYERS_INIT_POS[i][1] ]

        players[i]['color'] = [0, 0, 0]

        players[i]['moves'] = []

        players[i]['turns'] = []

        players[i]['index'] = i


    walls = [[0 for x in range(GAME_SIZE+1)] for y in range(GAME_SIZE+1)]


    keep_going = True

    winner = -2 # -2 -> undefined, -1-> tie, x -> id of winner

    while winner == -2:
        for index, player in enumerate(players):
            player['moves'].append([player['x'], player['y']])
            player['turns'].append(player['dir'])
            walls[player['x']][player['y']] = 1

            # move motorcycles
            if player['dir'] == 'N':
                player['y'] += 1
            if player['dir'] == 'E':
                player['x'] += 1
            if player['dir'] == 'S':
                player['y'] -= 1
            if player['dir'] == 'W':
                player['x'] -= 1

          


        if  player['x'] < 0 or player['x'] >= GAME_SIZE or \
            player['y'] < 0 or player['y'] >= GAME_SIZE or\
            walls[player['x']][player['y']] == 1 :

            if winner == -2:
                winner = 0 if index == 1 else 1
            else:
                winner = -1
                

        
        player['dir'] = lua_func_player_1(walls, player['x'], player['y'], player['dir'])
        print "Player ", index, " direction : ", player['dir']

            

    print 'game ends'
    return {'winner': winner, 'players': players }

    #return {'winner': winner, 'player1': {'moves': player_1['moves'], 'turns': player_1['turns'], 'initialPosition': [PLAYER_1_INITIAL_X, PLAYER_1_INITIAL_Y]}, 'player2': {'moves': player_2['moves'], 'turns': player_2['turns'], 'initialPosition': [PLAYER_2_INITIAL_X, PLAYER_2_INITIAL_Y]}}

        #direction_player_1 = lua_func_player_1(walls)
        #direction_player_2 = lua_func_player_1(walls)
