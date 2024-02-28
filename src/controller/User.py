from database.database import add_new_user, auth_user, get_user, update_user, get_user_id, get_user_by_id, get_user_backlog
from models.User import User
from flask import jsonify

def create_user(user: User):
    user_id = add_new_user(user)
    if user_id == "user already exists":
        return user_id
    else:
        user['user_id'] = user_id
        update_user(user)
        return user_id
    
def verify_user(user_email: str, user_password: str) -> bool:
    return auth_user(user_email, user_password)

def get_user_id_by_email(user_email: str):
    return get_user_id(user_email)

def search_user_by_id(user_id: str):
    user = get_user_by_id(user_id)
    games = get_user_backlog(user_id)

    if games['jogos'] != []:
        jogos = games['jogos']
    else:
        jogos = 'Nothing'
    if games['buy_list'] != []:
        buy_list = games['buy_list']
    else:
        buy_list = 'Nothing'

    result = {
        "user_id": user['user_id'],
        "user_name": user['user_name'],
        "user_email": user['user_email'],
        "backlog_games": jogos,
        "list_buy_games": buy_list,
        "wallet": games['wallet']
    }

    return result