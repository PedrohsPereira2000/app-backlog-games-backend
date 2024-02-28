import uvicorn
from flask import Flask, jsonify, request
from flask_cors import CORS
from models.User import User
from controller.User import create_user, verify_user, get_user_id_by_email, search_user_by_id

app = Flask(__name__)
CORS(app)

@app.route("/", methods=['GET'])
def test_root():
    return jsonify({'message': 'A rota está funcionando!'})

@app.route("/login", methods=['POST'])
def auth_user():
    data = request.json
    if 'user_email' in data and 'user_password' in data:
        if verify_user(data['user_email'], data['user_password']):
            return jsonify(
                {
                    "user_id": get_user_id_by_email(data['user_email'])
                }
            )
        else:
            return jsonify({"error": "Não foi possível logar o usuário"})

    else:
        return jsonify({"error": "Está fantando informação"})
    
@app.route("/user/<user_id>", methods=['GET'])
def get_backlog_by_user(user_id):
    user = search_user_by_id(user_id)
    if user is None:
        return jsonify({"error": "O Id do usuário não foi informado, ou está errado"})
    return jsonify(
        {"Success": user}
    )

if __name__ == "__main__":
    app.run(port=8999, debug=True)