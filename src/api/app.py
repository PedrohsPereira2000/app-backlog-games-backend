from flask import Flask, jsonify, request
from flask_cors import CORS
from models.User import User
from controller.User import create_user, verify_user, get_user_id_by_email, search_user_by_id

app = Flask(__name__)
CORS(app)

@app.route("/test_router", methods=['GET'])
def test_root():
    return jsonify({'message': 'A rota está funcionando!'})

@app.route("/login", methods=['POST'])
def auth_user():
    data = request.json
    print(data)
    if 'user_email' in data and 'user_password' in data:
        if verify_user(data['user_email'], data['user_password']):
            print(get_user_id_by_email(data['user_email']))
            return jsonify(
                {
                    "user_id": get_user_id_by_email(data['user_email'])
                }
            )
        else:
            return jsonify({"error": "Não foi possível logar o usuário"})

    else:
        return jsonify({"error": "Está fantando informação"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)