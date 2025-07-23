from fastapi import APIRouter, Depends,FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routes import chat


app=FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
   
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(chat.router)