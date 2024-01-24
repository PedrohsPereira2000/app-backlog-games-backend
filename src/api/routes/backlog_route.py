from fastapi import APIRouter, Body, status, HTTPException
from fastapi.responses import JSONResponse
from src.controller.Backlog import add_game, remove_game, update_game, find_game, update_status_game

router = APIRouter()

@router.post("/register")
async def register(backlog = Body(...)) -> JSONResponse:
    game = add_game(backlog)
    if game == "user already exists":
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
                "Status": game,
            }
        )

@router.post("/delete")
async def register(data = Body(...)) -> JSONResponse:
    game = remove_game(data)
    if game == "game not exists":
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "error": "game not exists",
            }
        )
    else:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "Status": game,
            }
        )
    
@router.post("/search")
async def register(data = Body(...)) -> JSONResponse:
    game = find_game(data)
    if game == "game not exists":
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "error": "game not exists",
            }
        )
    else:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "game":game,
            }
        )

@router.post("/update")
async def register(data = Body(...)) -> JSONResponse:
    game = update_game(data)
    if game == "game not exists":
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "error": "game not exists",
            }
        )
    else:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "response": game,
            }
        )
    
@router.post("/update/progress")
async def register(data = Body(...)) -> JSONResponse:
    game = update_status_game(data)
    if game == "game not exists":
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "error": "game not exists",
            }
        )
    else:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "response": game,
            }
        )