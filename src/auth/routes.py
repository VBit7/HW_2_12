from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

import database                         # noqa
import auth.repository as repo          # noqa
import auth.schemas as schemas          # noqa
import auth.services as services        # noqa


router = APIRouter(prefix="/auth", tags=["auth"])
get_refresh_token = HTTPBearer()


@router.post("/signup", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
async def signup(body: schemas.UserSchema, db: AsyncSession = Depends(database.get_db)):
    if not body.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Password is required"
        )
    exist_user = await repo.get_user_by_email(body.email, db)
    if exist_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Account already exists"
        )
    body.password = services.auth_service.get_password_hash(body.password)
    new_user = await repo.create_user(body, db)
    return new_user


@router.post("/login", response_model=schemas.TokenSchema)
async def login(
    body: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(database.get_db)
):
    user = await repo.get_user_by_email(body.username, db)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email"
        )
    if not services.auth_service.verify_password(body.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password"
        )
    access_token = await services.auth_service.create_access_token(
        data={"sub": user.email, "test": "Any_thing"}
    )
    refresh_token = await services.auth_service.create_refresh_token(data={"sub": user.email})
    await repo.update_token(user, refresh_token, db)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.get("/refresh_token", response_model=schemas.TokenSchema)
async def refresh_token(
    credentials: HTTPAuthorizationCredentials = Depends(get_refresh_token),
    db: AsyncSession = Depends(database.get_db),
):
    token = credentials.credentials
    email = await services.auth_service.decode_refresh_token(token)
    user = await repo.get_user_by_email(email, db)
    if user.refresh_token != token:
        await repo.update_token(user, None, db)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
        )
    access_token = await services.auth_service.create_access_token(data={"sub": email})
    refresh_token = await services.auth_service.create_refresh_token(data={"sub": email})
    await repo.update_token(user, refresh_token, db)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }
