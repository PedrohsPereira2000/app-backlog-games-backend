from dotenv import load_dotenv
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware
# from api.routes.user_routes import router as user_router
# from models.User import User
# from controller.User import create_user, verify_user, get_user_id_by_email, search_user_by_id

_ = load_dotenv()

app = FastAPI(
    middleware=[
        Middleware(
            CORSMiddleware,
            allow_origins=['*'],
            allow_credentials=True,
            allow_methods=['*'],
            allow_headers=['*']
        )
    ]
)

# app.include_router(
#     user_router, tags=["User"], prefix="/user"
# )

@app.get("/check")
def read_root():
    return {"Test Endpoint": "O endpoint está funcionando corretamente"}