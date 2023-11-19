"""Database operation support for Webapp."""

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import Field, SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession


class Member(SQLModel, table=True):
    """Member table."""
    name: str = Field(primary_key=True)
    secret: str


# DATABASE_URL = "sqlite:///./db/test.db"
DATABASE_URL = "sqlite+aiosqlite:///./db/test.db"
connect_args = {"check_same_thread": False}

engine = create_async_engine(
    DATABASE_URL, echo=True, future=True, connect_args=connect_args
)


async def create_db_and_tables():
    """Database initialization."""
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncSession:
    """Returns a database session."""
    async_session = sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
