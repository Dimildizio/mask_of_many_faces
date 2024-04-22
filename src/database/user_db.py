from sqlalchemy import select, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession

from src.constants import ASYNC_DB_URL

#ASYNC_DB_URL = 'sqlite+aiosqlite:///dnd_user_database.db'

Base = declarative_base()
async_engine = create_async_engine(ASYNC_DB_URL, echo=True)
async_session = sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)




class Character(Base):
    __tablename__ = 'characters'

    id = Column(Integer, primary_key=True, autoincrement=True)
    race = Column(String(50), default='dwarf')
    gender = Column(Boolean, default=False)
    dnd_class = Column(String(50), default='fighter')
    hair = Column(String(50), default='black')
    beard = Column(Boolean, default=True)
    background = Column(String(255), default='forest')

    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="character", uselist=False)


class Triplet(Base):
    __tablename__ = 'triplets'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    target_image = Column(String(255), nullable=True, default=None)
    face_image = Column(String(255), nullable=True, default=None)
    result_image = Column(String(255), nullable=True, default=None)

    character_id = Column(Integer, ForeignKey('characters.id'))
    character = relationship("Character")
    user = relationship("User", back_populates="triplets")


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, unique=True)
    user_name = Column(String(255), nullable=False)
    user_surname = Column(String(255), nullable=False)
    user_nickname = Column(String(255), nullable=True)

    is_premium = Column(Boolean, default=False)
    requests_left = Column(Integer, default=10)

    character_id = Column(Integer, ForeignKey('characters.id'))
    character = relationship("Character", back_populates="user", uselist=False)

    triplets = relationship("Triplet", back_populates="user", order_by=Triplet.id)


async def add_user(user_id, user_name, user_surname, user_nickname=None):
    async with async_session() as session:

        existing_user = await find_user_id(session, user_id)
        if existing_user:
            existing_user.user_name = user_name
            existing_user.user_surname = user_surname
            existing_user.user_nickname = user_nickname
        else:
            existing_user = User(
                user_id=user_id,
                user_name=user_name,
                user_surname=user_surname,
                user_nickname=user_nickname)
            existing_user.character = Character()
        session.add(existing_user)
        await session.commit()
        return existing_user


async def find_user_id(session, user_id):
    stmt = select(User).where(User.user_id == user_id)
    result = await session.execute(stmt)
    existing_user = result.scalars().first()
    return existing_user


async def fetch_user_data(user_id):
    """Fetch and print all data for a user by user_id."""
    async with async_session() as session:
        result = await session.get(User, user_id)
        if result:
            print(f"User Data: {result.__dict__}")
        else:
            print("User not found.")


async def fetch_user_details(user_id):
    """Fetch specific attributes for a user by user_id."""
    async with async_session() as session:
        stmt = select(
            User.dnd_class, User.race, User.beard, User.hair, User.background
        ).where(User.id == user_id)
        result = await session.execute(stmt)
        user_details = result.first()
        if user_details:
            print(user_details)
            print(f"Class: {user_details.dnd_class}, Race: {user_details.race}, Beard: {user_details.beard}, "
                  f"Hair: {user_details.hair}, Background: {user_details.background}")
        else:
            print("User details not found.")


async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
