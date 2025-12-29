from datetime import datetime, timezone
from fastapi import Request, Depends
from jose import jwt, JWTError, ExpiredSignatureError
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dao import UsersDAO
from app.auth.models import User
from app.config import settings
from app.dependencies.dao_dep import get_session_without_commit
from app.exceptions import (
    TokenNoFound, NoJwtException, TokenExpiredException, NoUserIdException, ForbiddenException, UserNotFoundException
)

def get_access_token(request: Request) -> str:
    """Extract access_token from cookies."""
    token = request.cookies.get('user_access_token')
    if not token:
        raise TokenNoFound
    return token

def get_refresh_token(request: Request) -> str:
    """Extract refresh_token from cookies."""
    token = request.cookies.get('user_refresh_token')
    if not token:
        raise TokenNoFound
    return token

async def check_refresh_token(
        token: str = Depends(get_refresh_token),
        session: AsyncSession = Depends(get_session_without_commit)
) -> User:
    """Verify refresh_token and return user."""
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        user_id = payload.get("sub")
        if not user_id:
            raise NoJwtException

        user = await UsersDAO(session).find_one_or_none_by_id(data_id=int(user_id))
        if not user:
            raise NoJwtException

        return user
    except JWTError:
        raise NoJwtException


async def get_current_user(
        token: str = Depends(get_access_token),
        session: AsyncSession = Depends(get_session_without_commit)
) -> User:
    """Verify access_token and return user."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except ExpiredSignatureError:
        raise TokenExpiredException
    except JWTError:
        raise NoJwtException

    user_id: str = payload.get('sub')
    if not user_id:
        raise NoUserIdException

    user = await UsersDAO(session).find_one_or_none_by_id(data_id=int(user_id))
    if not user:
        raise UserNotFoundException
    return user

# Admin role IDs: 3 = admin, 4 = super_admin
ADMIN_ROLE_IDS = [3, 4]

async def get_current_admin_user(current_user: User = Depends(get_current_user)) -> User:
    """Verify user has admin privileges."""
    if current_user.role.id in ADMIN_ROLE_IDS:
        return current_user
    raise ForbiddenException
