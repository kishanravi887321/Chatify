from fastapi import APIRouter, Depends,FastAPI

from src.api.routes import chat

app=FastAPI()
app.include_router(chat.router)