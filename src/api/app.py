from fastapi import FastAPI
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from api.routes.user_route import router as UserRouter
from api.routes.backlog_route import router as BacklogRouter

app = FastAPI(
    middleware=[
        Middleware(
            CORSMiddleware,
            allow_origins=["https://app-backlog-games-frontend-1e9i.vercel.app"],
            allow_methods=["*"],
            allow_headers=["*"],
            allow_credentials=True,
        )
    ]
)

app.include_router(
    UserRouter, tags=["UserRouter"], prefix="/user"
    )

app.include_router(
    BacklogRouter, tags=["BacklogRouter"], prefix="/backlog"
)