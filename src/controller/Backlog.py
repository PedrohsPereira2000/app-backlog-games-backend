from database.database import *
from datetime import date
from flask import jsonify

def add_game(data: dict):
    user_id = data['user_id']
    data = data['game']
    resp = add_new_game(data, user_id)
    return resp

def buying_game(user_id, data: dict):
    print(data)
    user_id = user_id
    price = data['price']
    data = data['game']
    resp = add_new_game(data, user_id)
    calc_wallet(user_id, price)
    add_game_buy_list(user_id, data['id'], data['name'], price)
    return resp

def calc_wallet(user_id, price):
    refectory_wallet(user_id, price)

def create_new_backlog(user):
    resp = new_backlog(user)

def remove_game(data: dict, user_id):
    resp = delete_game(data['id'], user_id)
    resp2 = delete_buy_game(data['id'], user_id)
    return resp

def update_game(data: dict, user_id):
    resp = up_game(user_id, data['game'])
    return resp


def find_game(data: dict):
    result = search_game(data['user_id'], data['id'])
    return result

def update_status_game(data: dict):
    origin_game = search_game(data['user_id'], data['game']['id'])
    if data['type'] == 'finished':
        origin_game['finished'] = True
        origin_game['data_finished'] = date.today().isoformat()
        update_earned(data['user_id'], data['game']['id'], 50)
    elif data['type'] == 'platinum':
        if origin_game['finished'] == False:
            origin_game['finished'] = True
            origin_game['data_finished'] = date.today().isoformat()
            update_earned(data['user_id'], data['game']['id'], 50)
        origin_game['platinum'] = True
        origin_game['data_platinum'] = date.today().isoformat()
        update_earned(data['user_id'], data['game']['id'], 30)
    up_game(data['user_id'], origin_game) 
    return 'Game Finished Successfully'

def number_of_games(userId: str):
    return count_games(userId)