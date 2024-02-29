import asyncio
# from fastapi import APIRouter, Body, status, HTTPException
# from fastapi.responses import JSONResponse
from flask import Blueprint, jsonify, request
from models.User import User
from controller.User import create_user, verify_user, get_user_id_by_email, search_user_by_id

user_bp = Blueprint('user', __name__)

@user_bp.route("/login", methods=['POST'])
async def auth_user():
    data = request.json
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
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"unauthorized"}
            )

# @user_bp.route("/{user_id}", methods=['GET'])
# async def get_user():
#     user = search_user_by_id(user_id)
#     if user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return JSONResponse(
#         status_code=status.HTTP_200_OK,
#         content={"user": user}
#         )

# @user_bp.route("/update", methods=['POST'])
# async def update_user():
#     return JSONResponse(
#         status_code=status.HTTP_200_OK,
#         content={user['user_name']: "updated"}
#         )

# @user_bp.route("/register", methods=['POST'])
# async def register():
#     user = create_user(user)
#     if user == "user already exists":
#         return JSONResponse(
#             status_code=status.HTTP_409_CONFLICT,
#             content={
#                 "error": "user already exists",
#             }
#         )
#     else:
#         return JSONResponse(
#             status_code=status.HTTP_201_CREATED,
#             content={
#                 "created_user": user.user_id,
#             }
#         )

