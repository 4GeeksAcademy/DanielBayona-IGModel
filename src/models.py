import os
import sys
import enum
from sqlalchemy import Column, ForeignKey, Integer, String, Date, Enum
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key = True)
    username = Column(String(50), nullable=False, unique=True)
    firstname = Column(String(20), nullable=False, unique=False)
    lastname = Column(String(20), nullable=False, unique=False)
    email = Column(String(40), nullable=False, unique=True)
    birth_date = Column(Date, nullable=False)

    post = relationship('Post', back_populates='author', cascade='all, delete')
    followers = relationship('User_Follower', back_populates='user')
    following = relationship('User_Follower', back_populates='followers')

class User_Follower(Base):
    __tablename__ = 'user_follower'
    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    follower_id = Column(Integer, ForeignKey('user.id'), primary_key=True)

    user = relationship('User', back_populates='followers')
    followers = relationship('User', back_populates='following')
    user_feed = relationship('User_Feed')

class Feed(Base):
    __tablename__ = 'feed'
    id = Column(Integer, primary_key = True)
    content = Column(String(20), nullable=False, unique=True)
    title = Column(String(20), nullable=False, unique=False)
    uploaded = Column(Integer, nullable=False, unique=True)
    user_feed = relationship('User_Feed')

class User_Feed(Base):
    __tablename__ = 'user_feed'
    id = Column(Integer, primary_key = True)
    user_id = Column(Integer, ForeignKey('user.id'))
    feed_id = Column(Integer, ForeignKey('feed.id'))

    user = relationship('User')
    feed =relationship('Feed')

class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key = True)
    title = Column(String, nullable = False, unique = False)
    content = Column(String, nullable = False, unique = False)
    user_id = Column(Integer, ForeignKey('user.id'))

    author = relationship('User', back_populates='post')
    media = relationship('Media', back_populates='media')

class MediaEnum(enum.Enum):
    png ='png'
    jpeg = 'jpeg'
    mp4 = 'mp4'
    mp3 = 'mp3'

class Media(Base):
    __tablename__ = 'media'
    id=Column(Integer, primary_key=True)
    type = Column(Enum(MediaEnum))
    url = Column(String(100), nullable=False, unique=True)
    post_id = Column(Integer, ForeignKey('post.id'))

    media = relationship('Post', back_populates='media')
## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e
