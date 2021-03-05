from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from database import Base
from auth.models import User
import datetime

class Credential(Base):
    __tablename__ = 'credentials'
    id = Column(Integer, primary_key=True)
    user = Column(Integer, ForeignKey('users.id'),nullable=False)
    url = Column(String(256), nullable=False)
    name = Column(String(30), nullable=True)
    username = Column(String(30), nullable=False)
    password = Column(String(20), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return '<User %r>' % self.username

    def __init__(self, user, url, name, username, password):
        self.user = user
        if 'http' not in url:
            url = 'http://' + url
        self.url = url
        self.name = name
        self.username = username
        self.password = password