from database.database import *
from flask import jsonify

def add_game(data: dict):
    user_id = data['user_id']
    data = data['game']
    resp = add_new_game(data, user_id)
    return resp

def buying_game(user_id, data: dict):
    user_id = user_id
    data = data['game']
    resp = add_new_game(data, user_id)
    calc_wallet(user_id, data['price'])
    add_game_buy_list(user_id, data)
    return resp

def calc_wallet(user_id, price):
    refectory_wallet(user_id, price)

def create_new_backlog(user):
    resp = new_backlog(user)

def remove_game(data: dict):
    resp = delete_game(data['id'], data['user_id'])
    resp2 = delete_buy_game(data['id'], data['user_id'])
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
            update_earned(data['user_id'], data['game']['id'], 50)
        else:
            update_earned(data['user_id'], data['game']['id'], 25)
    elif data['type'] == 'platinum':
        if origin_game['finished'] == False:
            origin_game['finished'] = True
            origin_game['hours'] = data['game']['hours']
            if data['game']['hours'] >= 25:
                update_earned(data['user_id'], data['game']['id'], 50)
            else:
                update_earned(data['user_id'], data['game']['id'], 25)
        else:
            origin_game['hours'] += data['game']['hours']
        origin_game['platinum'] = True
        up_game(data['user_id'], origin_game)
        if data['game']['hours'] >= 40:
            update_earned(data['user_id'], data['game']['id'], 50)
        elif data['game']['hours'] >= 20 and data['game']['hours'] < 40:
            update_earned(data['user_id'], data['game']['id'], 30)
        else:
            update_earned(data['user_id'], data['game']['id'], 15)
    return 'Game Finished Successfully'

def number_of_games(userId: str):
    return count_games(userId)