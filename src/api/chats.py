from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

# Flexible imports to handle different deployment scenarios

from src.api.store import ChatifyService
from src.db.utils import ExistUser
from ..db.dep import get_db  # get_db yields SessionLocal

   

router = APIRouter(prefix="/chat", tags=["Chatify1"])

# Request Models
class QueryRequest(BaseModel):
    query: str
    email: str

class UpsertRequest(BaseModel):
    raw_text: str
    email: EmailStr
   


@router.get("/")
def health_check():
    return {"status": "ok"}

@router.post("/get/")
def ask_question(payload: QueryRequest):
    response, status_code = ChatifyService.handle_query(api_key=payload.email, query=payload.query)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=response.get("message"))
    print(type(response))  # Ensure response is a dictionary   
    return response


@router.post("/feed/")
def upsert_data(payload: UpsertRequest, db: Session = Depends(get_db)):
    if not ExistUser(payload.email).check_user_exists(db):
        raise HTTPException(status_code=501, detail="User does not exist")

   

    response, status_code = ChatifyService.upsert_text_and_generate_api_key(
        raw_text=payload.raw_text,
        email=payload.email,
     
    )
    if status_code != 201:
        raise HTTPException(status_code=status_code, detail=response.get("message"))
    print(response)  # Ensure response is a dictionary
    return response