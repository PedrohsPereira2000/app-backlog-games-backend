from fastapi import APIRouter, Body, status, HTTPException
from fastapi.responses import JSONResponse
from models.User import User
from controller.User import create_user, verify_user, get_user_id_by_email, search_user_by_id

router = APIRouter()

@router.post("/login")
def auth_user(user = Body(...)):
    if user['user_email'] != '' and user['user_password'] != '':
        if verify_user(user['user_email'], user['user_password']):
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "Response":"loged in app",
                    "user_id": get_user_id_by_email(user['user_email'])}
                )
        else:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"unauthorized"}
                )

    else:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"unauthorized"}
            )

@router.get("/{user_id}")
def get_user(user_id: str):
    user = search_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"user": user}
        )

@router.post("/update")
def update_user(user = Body(...)):
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={user['user_name']: "updated"}
        )

@router.post("/register")
def register(user: User = Body(...)) -> JSONResponse:
    user = create_user(user)
    if user == "user already exists":
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "error": "user already exists",
            }
        )
    else:
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "created_user": user.user_id,
            }
        )

@router.get("/0/test_router")
def verify():
    return "O SERVIÇO DE ROTAS ESTÁ FUNCIONANDO"
