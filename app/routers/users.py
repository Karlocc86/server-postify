

import uuid

from fastapi import APIRouter, Depends, HTTPException

from typing import List

from sqlmodel import select

from app.models.user import User


from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_session
from app.schemas.user import UserCreate, UserRead, UserUpdate


router = APIRouter(prefix="/users", tags=["users"])

@router.get('/', response_model=List[UserRead])

async def get_users(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User))
    return result.scalars().all()

@router.post('/', response_model = UserRead, status_code=201)

async def create_user(data:UserCreate,session: AsyncSession = Depends(get_session)):
    user = User(**data.model_dump())
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user

@router.put('/{user_id}', response_model=UserRead, status_code=200)

async def update_user(user_id: uuid.UUID, data: UserUpdate, session: AsyncSession = Depends(get_session)):
    user = User(**data.model_dump())
    user.id = user_id
    result = await session.execute(select(User).where(User.id == user_id))
    existing_user = result.scalar_one_or_none()
    if not existing_user:
        raise HTTPException(status_code=404, detail="usuario no encontrado")
    for key, value in data.model_dump().items():
        setattr(existing_user, key, value)
    session.add(existing_user)
    await session.commit()
    await session.refresh(existing_user)
    return existing_user

@router.delete('/{user_id}', status_code=204)

async def delete_user(user_id: uuid.UUID, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User).where(User.id == user_id))
    existing_user = result.scalar_one_or_none()
    if not existing_user:
        raise HTTPException(status_code=404, detail="usuario no encontrado")
    await session.delete(existing_user)
    await session.commit()