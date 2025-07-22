from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
load_dotenv()

import os 
Db_url=os.getenv('DB_URL')

engine = create_engine(Db_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

