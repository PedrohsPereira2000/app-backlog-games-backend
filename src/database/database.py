import pymongo
from decouple import config
from fastapi.encoders import jsonable_encoder
from src.models.User import User

client = pymongo.MongoClient(config('MONGO_URI'))
db = client[config('MONGO_DATABASE')]
user_collection = db['users']
backlog_collection = db['backlog']

def add_new_user(user: User):
    verify = get_user(user.user_email)
    if verify == None:
        result = user_collection.insert_one(jsonable_encoder(user))
        return str(result.inserted_id)
    else:
        return "user already exists"
    
def auth_user(user_email: str, user_password: str) -> bool:
    result = get_user(user_email)

    if result:
        if result['user_password'] == user_password:
            return True
        else:
            return False    

def get_user(user_email: str):
    result = user_collection.find_one(
        {"user_email": user_email}
    )
    return result

def get_user_by_id(user_id: str):
    result = user_collection.find_one(
        {"user_id": user_id}
    )
    return result

def update_user(user: User):
    result = user_collection.update_one(
        {"user_email": user.user_email},
        {"$set": jsonable_encoder(user)}
    )
    return result

def get_user_id(user_email: str):
    result = user_collection.find_one(
        {"user_email": user_email}
    )
    return result['user_id']

def get_user_backlog(user_id: str):
    result = backlog_collection.find_one(
        {"user_id": user_id}
    )

    backlog = result.get('backlog', {})
    
    return backlog

def add_new_game(game, user_id: str):
    result1 = backlog_collection.find_one(
        {"user_id": user_id}
    )
    jogos = result1.get('backlog', {}).get('jogos', [])

    game['id'] = str(len(jogos) + 1)
    result = backlog_collection.update_one(
        {"user_id": user_id},
        {"$push": {"backlog.jogos": game}}
    )
    return "Game added successfully"

def delete_game(id: str, user_id: str):
    result = backlog_collection.update_one(
        {"user_id": user_id},
        {"$pull": {"backlog.jogos": {"id": id}}}
    )
    return "Game removed successfully"

def up_game(user_id: str, game):
    result = backlog_collection.update_one(
        {"user_id": user_id, "backlog.jogos.id": game['id']},
        {"$set": {"backlog.jogos.$": game}}
    )
    return "Game updated successfully"

def search_game(user_id: str, game_id: str):
    result = backlog_collection.find_one(
        {"user_id": user_id}
    )
    jogos = result.get('backlog', {}).get('jogos', [])
    for jogo in jogos:
        if jogo['id'] == game_id:
            return jogo
    return "game not exists"

def update_wallet(user_id, value):
    result = backlog_collection.update_one(
        {"user_id": user_id},
        {"$inc": {"backlog.wallet": value}}
    )
    return "Wallet updated successfully"