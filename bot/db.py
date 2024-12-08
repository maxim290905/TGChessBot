from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import bcrypt

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password_hash = Column(String)

def get_session(database_url="sqlite:///chess.db"):
    engine = create_engine(database_url)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()

session = get_session()

def register_user(username, password):
    if session.query(User).filter_by(username=username).first():
        return "Пользователь уже существует."
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    user = User(username=username, password_hash=hashed_password.decode())
    session.add(user)
    session.commit()
    return "Пользователь успешно зарегистрирован!"

def authenticate_user(username, password):
    user = session.query(User).filter_by(username=username).first()
    if user and bcrypt.checkpw(password.encode(), user.password_hash.encode()):
        return user
    return None
