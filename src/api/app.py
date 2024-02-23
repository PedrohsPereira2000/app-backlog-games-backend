from fastapi import FastAPI
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from api.routes.user_route import router as UserRouter
from api.routes.backlog_route import router as BacklogRouter

middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )
]

app = FastAPI(middleware=middleware)

app.include_router(
    UserRouter, tags=["UserRouter"], prefix="/user"
    )

app.include_router(
    BacklogRouter, tags=["BacklogRouter"], prefix="/backlog"
)

@app.get("/test_router")
def test_root():
    return {"OK": "As rotas estão funcionando"}

origins=["https://app-backlog-games-frontend-1e9i.vercel.app"]


# app = FastAPI(
#     middleware=[
#         Middleware(
#             CORSMiddleware,
#             allow_origins=["https://app-backlog-games-frontend-1e9i.vercel.app"],
#             allow_methods=["GET", "POST", "OPTIONS"],
#             allow_headers=["*"],
#             allow_credentials=True,
#         )
#     ]
# )

# # handle CORS preflight requests
# @app.options('/{rest_of_path:path}')
# async def preflight_handler(request: Request, rest_of_path: str) -> Response:
#     response = Response()
#     response.headers['Access-Control-Allow-Origin'] = ALLOWED_ORIGINS
#     response.headers['Access-Control-Allow-Methods'] = 'POST, GET, DELETE, OPTIONS'
#     response.headers['Access-Control-Allow-Headers'] = 'Authorization, Content-Type'
#     return response

# # set CORS headers
# @app.middleware("http")
# async def add_CORS_header(request: Request, call_next):
#     response = await call_next(request)
#     response.headers['Access-Control-Allow-Origin'] = ALLOWED_ORIGINS
#     response.headers['Access-Control-Allow-Methods'] = 'POST, GET, DELETE, OPTIONS'
#     response.headers['Access-Control-Allow-Headers'] = 'Authorization, Content-Type'
#     return response
