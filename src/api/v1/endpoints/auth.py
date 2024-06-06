from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Body, Request, Depends, HTTPException, Response, status  # noqa
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

import crud, models, schemas  # noqa
from api import deps  # noqa
from core import security  # noqa
from core.config import settings  # noqa
from core.security import get_password_hash  # noqa
from core.utils import (  # noqa
    generate_password_reset_token,  # noqa
    send_reset_password_email,  # noqa
    verify_password_reset_token,  # noqa
)

router = APIRouter()


def get_tokens(sub):
    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(
        minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)

    response = ORJSONResponse(content={
        'access_token': security.create_access_token(
            sub, expires_delta=access_token_expires
        ),
        'token_type': 'bearer',
    })
    response.set_cookie(
        key="refresh-token",
        value=security.create_refresh_token(
            sub, expires_delta=refresh_token_expires
        )
    )
    return response


@router.post('/access-token', response_model=schemas.Token)
async def login_access_token(
    db: AsyncSession = Depends(deps.get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    '''
    OAuth2 compatible token login, get an access token for future requests
    '''
    user = await crud.user.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Incorrect email or password')
    elif not crud.user.is_active(user):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Inactive user')
    return get_tokens(user.id)


@router.post('/refresh-token', response_model=schemas.Token)
async def refresh_token(
    request: Request,
    response: Response,
    db: AsyncSession = Depends(deps.get_db),
) -> Any:
    '''
    Refresh token
    '''
    token = request.cookies.get('refresh-token')

    user_id = int(verify_password_reset_token(token))
    if not user_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Invalid token')
    user = await crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='The user with this ID does not exist in the system.',
        )
    elif not crud.user.is_active(user):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Inactive user')
    return get_tokens(user.id)


@router.post('/test-token', response_model=schemas.User)
async def test_token(
    current_user: models.User = Depends(deps.get_current_user)
) -> Any:
    '''
    Test access token
    '''
    return current_user


@router.post('/password-recovery/{email}', response_model=schemas.Msg)
async def recover_password(
    email: str, db: AsyncSession = Depends(deps.get_db)
) -> Any:
    '''
    Password Recovery
    '''
    user = await crud.user.get_by_email(db, email=email)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='The user with this email does not exist in the system.',
        )
    password_reset_token = generate_password_reset_token(email=email)
    send_reset_password_email(
        email_to=user.email, email=email, token=password_reset_token
    )
    return {'msg': 'Password recovery email sent'}


@router.post('/reset-password/', response_model=schemas.Msg)
async def reset_password(
    token: str = Body(...),
    new_password: str = Body(...),
    db: AsyncSession = Depends(deps.get_db),
) -> Any:
    '''
    Reset password
    '''
    user_id = int(verify_password_reset_token(token))
    if not user_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Invalid token')
    user = await crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='The user with this username does not exist in the system.',
        )
    elif not crud.user.is_active(user):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Inactive user')
    hashed_password = get_password_hash(new_password)
    user.hashed_password = hashed_password
    db.add(user)
    await db.commit()
    return {'msg': 'Password updated successfully'}
