import datetime

from aiogram import types
from gino import Gino
from sqlalchemy import Column, Sequence, sql, DateTime, TIMESTAMP, Interval, FLOAT
from sqlalchemy import BigInteger, String, Integer, ForeignKey, Time
from sqlalchemy.orm import relationship

from data.gui_config import USERS_PAGE_VOLUME, SONGS_PAGE_VOLUME, CHORDS_PAGE_VOLUME, COVERS_PAGE_VOLUME
from data.structure_config import AUDIO_DIR_PATH

db = Gino()


class User(db.Model):
    __tablename__ = "users"
    query: sql.Select

    id = Column(Integer, Sequence("user_id_seq"), primary_key=True)
    user_id = Column(BigInteger, unique=True)
    username = Column(String(255), unique=True)

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
    name = Column(String(10))
    song_id = Column(Integer, ForeignKey('songs.id'))
    start = Column(FLOAT)
    end = Column(FLOAT)

    song = relationship("Song", back_populates="chords")


class Cover(db.Model):
    __tablename__ = "covers"
    query: sql.Select

    id = Column(Integer, Sequence("cover_id_seq"), primary_key=True)
    name = Column(String(255))
    song_id = Column(Integer, ForeignKey('songs.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    date = Column(DateTime)
    accuracy = Column(Integer)
    file_name = Column(String(255), unique=True)

    song = relationship("Song", back_populates="covers")
    user = relationship("User", back_populates="covers")


class Subscription(db.Model):
    __tablename__ = "subscriptions"
    query: sql.Select

    id = Column(Integer, Sequence("subscription_id_seq"), primary_key=True)
    subscribed_id = Column(Integer, ForeignKey('users.id'))
    subscriber_id = Column(Integer, ForeignKey('users.id'))

    subscribed = relationship("User", back_populates="subscribers")


class DBCommands:
    # USERS ###########################3
    async def create_user(self):
        user = types.User.get_current()

        old_user = await self.get_user_by_chat_id(user.id)
        if old_user:
            return old_user

        new_user = User()
        new_user.user_id = user.id
        new_user.username = user.username

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

    # SONGS ########################################################################
    async def get_song(self, song_id):
        song = await Song.get(song_id)
        return song

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

    async def get_user_songs_list(self, user_id, page_num):
        return await Song.query.where(Song.user_id == user_id).order_by(Song.author, Song.name).limit(
            SONGS_PAGE_VOLUME). \
            offset(page_num * SONGS_PAGE_VOLUME).gino.all()

    async def count_user_songs_list_pages(self, user_id):
        return int(await self.count_user_songs(user_id) / (SONGS_PAGE_VOLUME + 1))

    async def count_user_songs(self, user_id):
        return await db.select([db.func.count(Song.id)]).where(Song.user_id == user_id).gino.scalar()

    async def delete_song(self, song_id):
        song = await self.get_song(song_id)

        chords = await self.get_song_chords(song_id)
        for chord in chords:
            await chord.delete()
        await song.delete()

    # CHORDS #################

    async def create_chord(self, song_id, name, start, end):
        chord = Chord()
        chord.name = name
        chord.song_id = song_id
        chord.start = start
        chord.end = end
        await chord.create()

        return chord

    async def get_song_chords(self, song_id):
        return await Chord.query.where(Chord.song_id == song_id).gino.all()

    async def get_chords_list(self, song_id, page_num):
        return await Chord.query.where(Chord.song_id == song_id).order_by(Chord.start, Chord.end).limit(
            CHORDS_PAGE_VOLUME). \
            offset(page_num * CHORDS_PAGE_VOLUME).gino.all()

    async def count_song_chords(self, song_id):
        return await db.select([db.func.count(Chord.id)]).where(Chord.song_id == song_id).gino.scalar()

    async def count_chords_list_pages(self, song_id):
        return int(await self.count_song_chords(song_id) / (CHORDS_PAGE_VOLUME + 1))

    # COVERS ###################33

    async def create_cover(self, song_id, user_id, name):
        cover = Cover()
        cover.song_id = song_id
        cover.name = name
        cover.date = datetime.datetime.now()
        cover.user_id = user_id
        await cover.create()
        file_name = AUDIO_DIR_PATH + 'cover' + str(cover.id) + '.wav'
        await cover.update(file_name=file_name).apply()
        return cover

    async def get_cover(self, cover_id):
        cover = await Cover.get(cover_id)
        return cover

    async def get_user_covers_page(self, user_id, page_num):
        return await Cover.query.where(Cover.user_id == user_id).order_by(Cover.date, Cover.name).limit(
            COVERS_PAGE_VOLUME). \
            offset(page_num * COVERS_PAGE_VOLUME).gino.all()

    async def count_user_covers(self, user_id):
        return await db.select([db.func.count(Cover.id)]).where(Cover.user_id == user_id).gino.scalar()

    async def get_user_song_covers(self, user_id, song_id):
        return await Cover.query.where((Cover.user_id == user_id) & (Cover.song_id == song_id)). \
            order_by(Cover.date, Cover.name).gino.all()

    # FRIENDS #####################

    async def create_subscription(self, subscribed_id, subscriber_id):
        subscription = Subscription()
        subscription.subscribed_id = subscribed_id
        subscription.subscriber_id = subscriber_id
        await subscription.create()

        return subscription

    async def get_user_subscriptions(self, user_id):
        return await db.select([User]).select_from(Subscription.join(User, (Subscription.subscribed_id == User.id))) \
            .where(Subscription.subscriber_id == user_id).gino.all()


db_api = DBCommands()
