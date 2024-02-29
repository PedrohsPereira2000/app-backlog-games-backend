from database.database import*
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

    result = {
        "user_id": user['user_id'],
        "user_name": user['user_name'],
        "user_email": user['user_email'],
        "backlog_games": games['jogos'],
        "list_buy_games": games['buy_list'],
        "wallet": calc_wallet(user_id)
    }

    print(result)

    return result