"""Webapp's query and response models."""

from pydantic import BaseModel


class Member(BaseModel):
    """Response member model."""
    name: str


class MemberCreate(BaseModel):
    """Member create request model."""
    name: str
    secret: str
