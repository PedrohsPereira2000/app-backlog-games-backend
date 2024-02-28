from database.database import add_new_game, delete_game, up_game, search_game, update_wallet, new_backlog
from flask import jsonify

def add_game(data: dict):
    user_id = data['user_id']
    data = data['game']
    resp = add_new_game(data, user_id)
    return resp

def create_new_backlog(user):
    resp = new_backlog(user)

def remove_game(data: dict):
    resp = delete_game(data['id'], data['user_id'])
    return resp

def update_game(data: dict):
    resp = up_game(data['user_id'], data['game'])
    return resp

def find_game(data: dict):
    result = search_game(data['user_id'], data['id'])
    return result

def update_status_game(data: dict):
    origin_game = search_game(data['user_id'], data['game']['id'])
    # verificar se o jogo foi zerado ou platinado
    if data['type'] == 'finished':
        origin_game['finished'] = True
        origin_game['hours'] = data['game']['hours']
        up_game(data['user_id'], origin_game)
        if data['game']['hours'] >= 25:
            update_wallet(data['user_id'], 50)
        else:
            update_wallet(data['user_id'], 25)
    elif data['type'] == 'platinum':
        if origin_game['finished'] == False:
            origin_game['finished'] = True
            if data['game']['hours'] >= 25:
                update_wallet(data['user_id'], 50)
            else:
                update_wallet(data['user_id'], 25)
        origin_game['platinum'] = True
        origin_game['hours'] = data['game']['hours']
        up_game(data['user_id'], origin_game)
        if data['game']['hours'] >= 40:
            update_wallet(data['user_id'], 50)
        elif data['game']['hours'] >= 20 and data['game']['hours'] < 40:
            update_wallet(data['user_id'], 30)
        else:
            update_wallet(data['user_id'], 15)
    return 'Game Finished Successfully'