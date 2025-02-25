﻿from datetime import datetime, timedelta  # noqa
from typing import Any, Union  # noqa

from jose import jwt
from passlib.context import CryptContext

from core.config import settings  # noqa


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def create_access_token(
    subject: Union[str, Any], expires_delta: timedelta = None
) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {'exp': expire, 'sub': str(subject)}
    encoded_jwt = jwt.encode(to_encode,
                             settings.SECRET_KEY,
                             algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


def create_refresh_token(
    subject: Union[str, Any], expires_delta: timedelta = None
) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {'exp': expire, 'sub': str(subject)}
    print()
    print(settings.SECRET_KEY)
    print()
    encoded_jwt = jwt.encode(to_encode,
                             settings.SECRET_KEY,
                             algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
