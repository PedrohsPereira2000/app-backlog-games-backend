from flask import Flask, jsonify, request
from flask_cors import CORS
from models.User import User
from controller.User import *
from controller.Backlog import *

app = Flask(__name__)
CORS(app)

@app.route("/", methods=['GET'])
def test():
    return jsonify({'message': 'A rota está funcionando!'}), 200

@app.route("/login", methods=['POST'])
def login():
    data = request.json
    if 'user_email' in data and 'user_password' in data:
        if verify_user(data['user_email'], data['user_password']):
            return jsonify(
                {
                    "user_id": get_user_id_by_email(data['user_email'])
                }
            ),200
        else:
            return jsonify({"error": "Não foi possível logar o usuário"}), 400

    else:
        return jsonify({"error": "Está fantando informação"})
    
@app.route("/user/<user_id>", methods=['GET'])
def get_backlog_by_user(user_id):
    user = search_user_by_id(user_id)
    if user is None:
        return jsonify({"error": "O Id do usuário não foi informado, ou está errado"})
    return jsonify(
        {"Success": user}
    ), 200

@app.route("/user/<user_id>/profile", methods=['GET'])
def get_profile_by_user(user_id):
    user = search_user_profile(user_id)
    if user is None:
        return jsonify({"error": "O Id do usuário não foi informado, ou está errado"})
    return jsonify(
        {"Success": user}
    ), 200

@app.route("/user/<user_id>/profile/update", methods=['POST'])
def update_user(user_id):
    user = request.json
    user_updated = update_user_profile(user)
    return jsonify({
        "OK": "User updated with sucess"
    }
), 200

@app.route("/user/register", methods=['POST'])
def register():
    user = request.json
    user = create_user(user)
    if user == "user already exists":
        return jsonify({
                "error": "user already exists",
            }
        ), 400
    else:
        create_new_backlog(user)
        return jsonify({
                "created_user": user,
            }
        ), 200

@app.route("/dashboard/<user_id>/count_games", methods=['GET'])
def counts_game(user_id):
    game =  number_of_games(user_id)
    if game == "user already exists":
        return jsonify({
                "error": "user already exists",
            }
        ), 409
    else:
        return jsonify({
                "count": game,
            }
        ), 201
    
@app.route("/dashboard/<user_id>/buy_game", methods=['POST'])
def buy_game(user_id):
    backlog = request.json
    game = buying_game(user_id, backlog)
    return jsonify({
            "Status": game,
        }
    ), 201

@app.route("/dashboard/<user_id>/search", methods=['POST'])
def search_game(user_id):
    data = request.json
    game = find_game(data)
    if game == "game not exists":
        return jsonify({
                "error": "game not exists",
            }
        ), 409
    else:
        return jsonify({
                "game":game,
            }
        )
    
@app.route("/dashboard/<user_id>/update", methods=['POST'])
def update_backlog_game(user_id):
    data = request.json
    game = update_game(data, user_id)
    if game == "game not exists":
        return jsonify({
                "error": "game not exists",
            }
        ), 409
    else:
        return jsonify({
                "response": game,
            }
        ), 200
    
@app.route("/dashboard/update/progress", methods=['POST'])
def update_progress():
    data = request.json
    game = update_status_game(data)
    if game == "game not exists":
        return jsonify({
                "error": "game not exists",
            }
        ), 409
    else:
        return jsonify({
                "response": game,
            }
        ), 200
    
@app.route("/dashboard/<user_id>/delete", methods=['POST'])
def delete_game(user_id):
    data = request.json
    game = remove_game(data, user_id)
    if game == "game not exists":
        return jsonify({
                "error": "game not exists",
            }
        ), 409
    else:
        return jsonify({
                "Status": game,
            }
        ), 200

if __name__ == "__main__":
    app.run(debug=True)