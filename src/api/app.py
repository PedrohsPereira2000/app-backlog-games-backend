from fastapi import FastAPI, Request
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from api.routes.user_route import router as UserRouter
from api.routes.backlog_route import router as BacklogRouter

app = FastAPI()

app.include_router(
    UserRouter, tags=["UserRouter"], prefix="/user"
    )

app.include_router(
    BacklogRouter, tags=["BacklogRouter"], prefix="/backlog"
)

@app.get("/test_router")
def test_root():
    return {"OK": "As rotas estão funcionando"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)
