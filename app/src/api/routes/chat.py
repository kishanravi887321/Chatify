from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from src.core.store import ChatifyService
from src.db.dep import get_db  # get_db yields SessionLocal
from src.db.utils import ExistUser

router = APIRouter(prefix="/api/chatify", tags=["Chatify"])

# Request Models
class QueryRequest(BaseModel):
    query: str
    api_key: str

class UpsertRequest(BaseModel):
    raw_text: str
    email: EmailStr
    project_name: str


@router.post("/ask")
def ask_question(payload: QueryRequest):
    response, status_code = ChatifyService.handle_query(api_key=payload.api_key, query=payload.query)
    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=response.get("message"))
    return response


@router.post("/upsert")
def upsert_data(payload: UpsertRequest, db: Session = Depends(get_db)):
    if not ExistUser(payload.email).check_user_exists(db):
        raise HTTPException(status_code=501, detail="User does not exist")

    response, status_code = ChatifyService.upsert_text_and_generate_api_key(
        raw_text=payload.raw_text,
        email=payload.email,
        project_name=payload.project_name
    )
    if status_code != 201:
        raise HTTPException(status_code=status_code, detail=response.get("message"))
    return response
