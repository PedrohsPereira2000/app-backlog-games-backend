import pymongo
from datetime import date
from decouple import config
from flask import jsonify
from models.User import User

client = pymongo.MongoClient(config('MONGO_URI'))
db = client[config('MONGO_DATABASE')]
user_collection = db['users']
backlog_collection = db['backlog']

def add_new_user(user: User):
    verify = get_user(user['user_email'])
    if verify == None:
        result = user_collection.insert_one(user)
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
        {"user_id": user['user_id']},
        {"$set": user}
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
    if result != None:
        backlog = result.get('backlog', {})
        return backlog
    else:
        return "Nothing"
    
def new_backlog(user_id: str):
    result = get_user_backlog(user_id)
    if result == 'Nothing':
        result = backlog_collection.insert_one({
            "user_id": user_id,
            "backlog": {
                "jogos": [],
                "buy_list": [],
                "wallet": 0
            }
        })

def add_game_buy_list(user_id, id, name, price):
    buy_in_date = date.today().isoformat()
    backlog_collection.update_one(
        {"user_id": user_id},  # Condição para encontrar o documento do usuário
        {"$push": {
            "backlog.buy_list": {
                "id": id,
                "buy_in": buy_in_date,  # Data de compra atual
                "name": name,   # Nome do jogo
                "price": price  # Preço do jogo
            }
        }},
        upsert=True  # Se o documento não existir, crie um novo
    )

def calc_wallet(user_id):
    result = backlog_collection.find_one(
        {"user_id": user_id}
    )
    all_buyed = 0
    all_earned = 0
    backlog = result.get('backlog', {})
    buy_list = backlog.get('buy_list', [])
    backlog_list = backlog.get('jogos', [])

    if buy_list:
        for buy in buy_list:
            all_buyed+=buy['price']
    if backlog_list:
        for game in backlog_list:
            all_earned+=game['earned']

    wallet = all_earned - all_buyed

    backlog_collection.update_one(
        {"_id": result["_id"]},
        {"$set": {"backlog.wallet": wallet}}
    )

    return wallet

def refectory_wallet(user_id, value):
    result = backlog_collection.find_one(
        {"user_id": user_id}
    )
    if result:
        current_wallet = result.get('wallet', 0)  # Se a carteira não existir, assuma que é 0

        new_wallet_value = current_wallet - value

        # Atualize a carteira no banco de dados
        backlog_collection.update_one(
            {"_id": result["_id"]},
            {"$set": {"backlog.wallet": new_wallet_value}}
        )

        return new_wallet_value
    else:
        # Trate o caso em que o usuário não é encontrado
        return None

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

def delete_buy_game(id: str, user_id: str):
    result = backlog_collection.update_one(
        {"user_id": user_id},
        {"$pull": {"backlog.buy_list": {"id": id}}}
    )
    return "Game removed successfully"

def up_game(user_id: str, game):
    result = backlog_collection.update_one(
        {"user_id": user_id, "backlog.jogos.id": game['id']},
        {"$set": {"backlog.jogos.$": game}}
    )
    return "Game updated successfully"

def count_games(user_id: str):
    result = backlog_collection.find_one(
        {"user_id": user_id}
    )
    backlog = result.get('backlog', {}).get('jogos', {})
    return len(backlog)

def search_game(user_id: str, game_id: str):
    result = backlog_collection.find_one(
        {"user_id": user_id}
    )
    jogos = result.get('backlog', {}).get('jogos', [])
    for jogo in jogos:
        if jogo['id'] == game_id:
            return jogo
    return "game not exists"

def update_earned(user_id, game_id, value):
    # Crie a condição de pesquisa para encontrar o documento do usuário com o jogo específico
    condition = {
        "user_id": user_id,
        "backlog.jogos.id": game_id
    }

    # Atualize o campo earned do jogo específico usando a condição de pesquisa
    result = backlog_collection.update_one(
        condition,
        {"$inc": {"backlog.jogos.$[element].earned": value}},
        array_filters=[{"element.id": game_id}]
    )

    if result.modified_count == 0:
        # Se nenhum documento foi modificado, provavelmente o usuário ou o jogo não existe
        raise Exception("Usuário ou jogo não encontrado")

    return "Earned updated successfully"