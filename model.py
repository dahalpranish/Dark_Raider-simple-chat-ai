from sqlalchemy import Column, Integer,String,ForeignKey
from database import Base
from sqlalchemy.orm import relationship

class user_resister(Base):
    __tablename__ = "user_collection"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    chat = relationship("user_chat",back_populates="user")
    title = relationship("user_title",back_populates="user")

class user_title(Base):
    __tablename__ = "chat_title"
    title_id =  Column(Integer, primary_key=True)
    title_text = Column(String)
    user_id = Column(Integer,ForeignKey("user_collection.id"))
    user = relationship("user_resister",back_populates="title")
    chats = relationship("user_chat",back_populates="title")


class user_chat(Base):
    __tablename__ = "Users_chat"
    chat_id = Column(Integer, primary_key=True)
    user_text = Column(String)
    server_text = Column(String)
    user_id = Column(Integer, ForeignKey("user_collection.id"))
    title_id = Column(Integer,ForeignKey("chat_title.title_id"))
    user= relationship("user_resister",back_populates="chat")
    title = relationship("user_title",back_populates="chats")


