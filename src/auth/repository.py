from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from libgravatar import Gravatar

import database                         # noqa
import contacts.models as models        # noqa
import auth.schemas as schemas          # noqa


async def get_user_by_email(email: str, db: AsyncSession = Depends(database.get_db)):
    statement = select(models.User).filter_by(email=email)
    user = await db.execute(statement)
    user = user.scalar_one_or_none()
    return user


async def create_user(body: schemas.UserSchema, db: AsyncSession = Depends(database.get_db)):
    avatar = None
    try:
        g = Gravatar(body.email)
        avatar = g.get_image()
    except Exception as err:
        print(err)

    new_user = models.User(**body.model_dump(), avatar=avatar)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


async def update_token(user: models.User, token: str | None, db: AsyncSession):
    user.refresh_token = token
    await db.commit()
