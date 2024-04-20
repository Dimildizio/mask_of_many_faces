from datetime import datetime, date
from sqlalchemy import select, Column, Integer, String, Boolean #  TIMESTAMP, Date, ForeignKey, func
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession

#from constants import ASYNC_DB_URL
ASYNC_DB_URL = f'sqlite+aiosqlite:///dnd_user_database.db'


Base = declarative_base()
async_engine = create_async_engine(ASYNC_DB_URL, echo=True)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, unique=True)
    user_name = Column(String(255), nullable=False)
    user_surname = Column(String(255), nullable=False)
    user_nickname = Column(String(255), nullable=True)

    is_premium = Column(Boolean, default=False)
    requests_left = Column(Integer, default=10)

    race = Column(String(50), default='human')
    gender = Column(Boolean, default=False)
    dnd_class = Column(String(50), default='fighter')
    hair = Column(String(50), default='black')
    beard = Column(Boolean, default=False)
    background = Column(String(255), default='forest')


async_session = sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)


async def add_user(user_id, user_name, user_surname, user_nickname=None):
    async with async_session() as session:
        new_user = User(
            user_id = user_id,
            user_name=user_name,
            user_surname=user_surname,
            user_nickname=user_nickname
        )
        session.add(new_user)
        await session.commit()
        return new_user.user_id


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
        # Correct the usage of select by not using a list
        stmt = select(
            User.dnd_class, User.race, User.beard, User.hair, User.background
        ).where(User.id == user_id)  # Ensure you are using the correct column for filtering
        result = await session.execute(stmt)
        user_details = result.scalars().first()  # Use scalars().first() to fetch the first result properly.
        if user_details:
            print(user_details)
            print(f"Class: {user_details.dnd_class}, Race: {user_details.race}, Beard: {user_details.beard}, "
                  f"Hair: {user_details.hair}, Background: {user_details.background}")
        else:
            print("User details not found.")


async def main():
    user_id = await add_user(1, 'John', 'Doe', 'Johnny')
    print(f"User ID: {user_id}")
    await fetch_user_data(user_id)
    await fetch_user_details(user_id)

async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


if __name__ == '__main__':
    import asyncio
    asyncio.run(main())

