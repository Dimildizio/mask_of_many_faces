from sqlalchemy import select, Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession

from utilities.constants import ASYNC_DB_URL

# ASYNC_DB_URL = 'sqlite+aiosqlite:///dnd_user_database.db'

Base = declarative_base()
async_engine = create_async_engine(ASYNC_DB_URL, echo=True)
async_session = sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, unique=True)
    user_name = Column(String(255), nullable=True)
    user_surname = Column(String(255), nullable=True)
    user_nickname = Column(String(255), nullable=True)

    is_premium = Column(Boolean, default=False)
    requests_left = Column(Integer, default=10)

    race = Column(String(50), default='dwarf')
    gender = Column(Boolean, default=True)
    dnd_class = Column(String(50), default='fighter')
    hair = Column(String(50), default='black')
    beard = Column(Boolean, default=False)
    background = Column(String(50), default='forest')

    current_face_image = Column(String(255), nullable=True)
    current_target_image = Column(String(255), nullable=True)
    current_result_image = Column(String(255), nullable=True)


async def fetch_all_users():
    """Retrieve all users from the database."""
    async with async_session() as session:
        result = await session.execute(select(User))
        users = result.scalars().all()
        return users


async def add_user(user_id, user_name, user_surname=False, user_nickname=False):
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
            User.dnd_class, User.race, User.beard, User.gender, User.hair, User.background,
            User.current_face_image, User.current_target_image, User.current_result_image).where(
                User.user_id == user_id)
        result = await session.execute(stmt)
        user_details = result.first()
        if user_details:
            classes = (f"Class: {user_details.dnd_class}, Race: {user_details.race}, Gender: {user_details.gender},"
                       f"Beard: {user_details.beard}, Hair: {user_details.hair}, Background: {user_details.background}")
            triplets = (user_details.current_face_image, user_details.current_target_image,
                        user_details.current_result_image)
            print(user_id, classes, triplets)
            return user_details
        else:
            print("User details not found.")


async def update_attr(user_id, attribute_name, new_value):
    async with async_session() as session:
        user = await find_user_id(session, user_id)
        print(user)
        await fetch_user_details(user_id)
        if user:
            if hasattr(user, attribute_name):
                setattr(user, attribute_name, new_value)
                await session.commit()

                return user
            else:
                print(f"Attribute '{attribute_name}' not found on User.")
                return False
        print("User not found.")
        return False


async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
