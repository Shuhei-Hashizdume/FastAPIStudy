import os
from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from pwdlib import PasswordHash

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)


def create_access_token(subject: str) -> str:
    secret_key = os.environ["JWT_SECRET_KEY"]

    expires_at = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": subject,
        "exp": expires_at,
    }

    encoded_token = jwt.encode(payload, secret_key, algorithm=ALGORITHM)
    return encoded_token


def decode_access_token(token: str) -> dict[str, Any]:
    secret_key = os.environ["JWT_SECRET_KEY"]
    payload = jwt.decode(token, secret_key, algorithms=[ALGORITHM])
    return payload
