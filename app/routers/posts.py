

import uuid

from fastapi import APIRouter, Depends , HTTPException

from typing import List

from sqlmodel import select

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.models.post import Post
from app.schemas.post import PostCreate, PostRead, PostUpdate



router = APIRouter(prefix="/posts", tags=["posts"])

@router.get('/', response_model=List[PostRead])

async def get_posts(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Post))

    return result.scalars().all()

@router.post('/', response_model = PostRead, status_code=201)

async def create_post(data:PostCreate,session: AsyncSession = Depends(get_session)):
    post = Post(**data.model_dump())
    session.add(post)
    await session.commit()
    await session.refresh(post)
    return post


@router.put('/{post_id}', response_model=PostRead, status_code=200)

async def update_post(post_id: uuid.UUID, data: PostUpdate, session: AsyncSession = Depends(get_session)):
    post = Post(**data.model_dump())
    post.id = post_id
    result = await session.execute(select(Post).where(Post.id == post_id))
    existing_post = result.scalar_one_or_none()
    print('existe un post')
    print(existing_post)
    if not existing_post:
        raise HTTPException(status_code=404, detail="Post not found")
    for key, value in data.model_dump().items():
        setattr(existing_post, key, value)
    session.add(existing_post)
    await session.commit()
    await session.refresh(existing_post)
    return existing_post

@router.delete('/{post_id}', status_code=204)

async def delete_post(post_id: uuid.UUID, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Post).where(Post.id == post_id))
    existing_post = result.scalar_one_or_none()
    if not existing_post:
        raise HTTPException(status_code=404, detail="Post no existe o no lo encontre")
    await session.delete(existing_post)
    await session.commit()