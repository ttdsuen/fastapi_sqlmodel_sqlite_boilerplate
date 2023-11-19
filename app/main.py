"""Webapp main entry point."""
from typing import Optional

from fastapi import FastAPI, Depends
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

import database
import schema

# fastapi
app = FastAPI()


@app.on_event("startup")
async def on_startup():
    """Database initialization."""
    await database.create_db_and_tables()


@app.get("/members", response_model=list[schema.Member])
async def get_members(session: AsyncSession = Depends(database.get_session)):
    """Getting members."""
    members = await session.exec(select(database.Member))
    return [schema.Member(name=member.name) for member in members]


@app.post("/members", response_model=Optional[schema.Member])
async def add_member(
        member: schema.MemberCreate,
        session: AsyncSession = Depends(database.get_session)):
    """Add a given member."""
    member = database.Member(name=member.name, secret=member.secret)
    session.add(member)
    await session.commit()
    await session.refresh(member)
    return schema.Member(name=member.name)
