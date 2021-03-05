from sqlalchemy import Column, Integer, String, DateTime
from database import Base
import datetime

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(30), unique=True, nullable=False)
    password = Column(String(256), nullable=False)
    pin = Column(Integer, nullable=False)
    image = Column(String(256), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return '<User %r>' % self.username

    def __init__(self, username, password, pin, image_path):
        self.username = username
        self.password = password
        self.pin = pin
        self.image = image_path