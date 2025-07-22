from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.db.utils import ExistUser
from  src.db.dep import get_db
from sqlalchemy.orm import Session
from fastapi import Depends


app=FastAPI()

class NUmberInput(BaseModel):
     email:str


@app.post("/sqaure")
def square_number(input: NUmberInput,db:Session = Depends(get_db)):
   
    if ExistUser(input.email).check_user_exists(db):
        return {"message": "User exists"}

    