try:
    from .connect import SessionLocal
except ImportError:
    from connect import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

