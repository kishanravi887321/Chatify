try:
    from .handledb import User
except ImportError:
    from handledb import User


class ExistUser:
    def __init__(self, email: str):
        self.email = email


    def check_user_exists(self, db_session):
        return db_session.query(User).filter(User.email == self.email).first() is not None