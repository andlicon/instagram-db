import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er
import enum
from sqlalchemy import Enum

Base = declarative_base()


class TipoCuenta(enum.Enum):
    personal = 'personal',
    negocio = 'negocio'


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    nickname = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    email = Column(String(150), nullable=False, unique=True)
    name = Column(String(150), nullable=False)
    tipo_cuenta = Column(Enum(TipoCuenta), nullable=False, default=TipoCuenta.personal)
    img_url = Column(String(250))

    follower = relationship('Follower', back_populates='user')
    post = relationship('Post', back_populates='user')


    def serialize(self):
        return {
            "id": self.id,
            "nickname": self.nickname,
            "password": self.password,
            "email": self.email,
            "name": self.name,
            "tipo_cuenta": self.tipo_cuenta,
            "img_url": self.img_url
        }


class Follower(Base):
    __tablename__ = 'follower'

    id = Column(Integer, primary_key=True)
    user_id_follow = Column(Integer, ForeignKey('user.id'), nullable=False)
    user_id_following = Column(Integer, ForeignKey('user.id'), nullable=False)

    user = relationship('User', back_populates='follower')


    def serialize(self):
        return {
            "id": self.id,
            "user_id_follow": self.user_id_follow,
            "user_id_following": self.user_id_following
        }


class Post(Base):
    __tablename__ = 'post'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user_id'), nullable=False)
    location = Column(String(250))
    description = Column(String(250))

    user = relationship('User', back_populates='post')
    post_content = relationship('PostContent', back_populates='post')
    comment = relationship('Comment', back_populates='post')

    def serialize(self):
        return {
        "id": self.id,
        "user_id": self.user_id,
        "description": self.description
        }


class PostContent(Base):
    __tablename__ = 'post_content'

    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)
    url = Column(String(250), nullable=False)

    post = relationship('Post', back_populates='post_content')


    def serialize(self):
        return {
            "id": self.id,
            "post_id": self.post_id,
            "url": self.url
        }


class Publish(enum.Enum):
    comment = 'comment'
    post = 'post'


class Comment(Base):
    __tablename__ = 'comment'

    id = Column(Integer, primary_key=True)
    feedback_nature = Column(Enum(Publish), nullable=False)
    feedback_id = Column(Integer, nullable=False)
    text = Column(String(250), nullable=False)

    post = relationship('Post', back_populates='comment')
    comment = relationship('Comment', back_populates='comment')


    def serialize(self):
        return {
            "id": self.id,
            "feedback_nature": self.feedback_nature,
            "feedback_id": self.feedback_id,
            "text": self.text
        }


class Like(Base):
    __tablename__ = 'like'

    id = Column(Integer, primary_key=True)
    publish_nature = Column(Enum(Publish), nullable=False)
    publish_id = Column(Integer, nullable=False)

    post = relationship('Post', back_populates='like')
    comment = relationship('Comment', back_populates='like')


    def serialize(self):
        return {
            "id": self.id,
            "publish_nature": self.publish_nature,
            "publish_id": self.publish_id
        }
    

try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e
