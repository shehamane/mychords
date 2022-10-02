from aiogram import types
from gino import Gino
from sqlalchemy import Column, Sequence, sql
from sqlalchemy import Enum, BigInteger, String, Integer, ForeignKey, Time
from sqlalchemy.orm import relationship

from data.guitar_config import formations
from data.api_config import USERS_PAGE_VOLUME

db = Gino()


class User(db.Model):
    __tablename__ = "users"
    query: sql.Select

    id = Column(Integer, Sequence("user_id_seq"), primary_key=True)
    user_id = Column(BigInteger, unique=True)
    username = Column(String(255))

    songs = relationship("Song", back_populates="user")


class Song(db.Model):
    __tablename__ = "songs"
    query: sql.Select

    id = Column(Integer, Sequence("song_id_seq"), primary_key=True)
    name = Column(String(255))
    author = Column(String(255))
    duration = Column(Time())
    formation = Column(String(30))
    user_id = Column(Integer, ForeignKey('users.id'))
    file_name = Column(String(255), unique=True)

    user = relationship("User", back_populates="songs")
    chords = relationship("Chord", back_populates="songs")


class Chord(db.Model):
    __tablename__ = "chords"
    query: sql.Select

    id = Column(Integer, Sequence("chord_id_seq"), primary_key=True)
    name = Column(String(5))
    song_id = Column(Integer, ForeignKey('songs.id'))
    start = Column(Time())
    stop = Column(Time())

    song = relationship("Song", back_populates="chords")


class DBCommands:
    # USERS
    async def create_user(self):
        user = types.User.get_current()

        old_user = await self.get_user_by_chat_id(user.id)
        if old_user:
            return old_user

        new_user = User()
        new_user.user_id = user.id
        new_user.username = user.username
        new_user.balance = 0

        await new_user.create()
        return new_user

    async def get_current_user(self):
        user_id = types.User.get_current().id
        user = await self.get_user_by_chat_id(user_id)
        return user

    async def get_user(self, user_id):
        user = await User.get(user_id)
        return user

    async def count_users(self):
        total = await db.func.count(User.id).gino.scalar()
        return total

    async def get_user_by_chat_id(self, chat_id):
        user = await User.query.where(User.user_id == chat_id).gino.first()
        return user

    async def get_user_by_username(self, username):
        user = await User.query.where(User.username == username).gino.first()
        return user

    async def get_users_list(self, page_num):
        users_list = await User.query.order_by(User.username).limit(USERS_PAGE_VOLUME).offset(
            page_num * USERS_PAGE_VOLUME).gino.all()
        return users_list

    # CATEGORIES ########################################################################
    async def get_song(self, song_id):
        category = await Song.get(song_id)
        return category

    async def create_song(self, user_id, name, author, duration, file_name, formation='standard'):
        song = Song()
        song.name = name
        song.author = author
        song.duration = duration
        song.file_name = file_name
        song.user_id = user_id
        song.formation = formation
        await song.create()

        return song

    async def delete_song(self, id):
        song = await self.get_song(id)
        await song.delete()

    # CHORDS #################

    async def create_chord(self, name, song_id, start, stop):
        chord = Chord()
        chord.name = name
        chord.song_id = song_id
        chord.start = start
        chord.stop = stop

        return chord


db_api = DBCommands()
