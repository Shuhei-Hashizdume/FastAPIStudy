import logging

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt.exceptions import InvalidTokenError
from psycopg.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from database import get_db
from models import UserDB
from schemas import TokenResponse, UserCreate, UserLogin, UserResponse
from security import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)

router = APIRouter()
logger = logging.getLogger(__name__)
bearer_scheme = HTTPBearer()


def authenticate_user(email: str, password: str, db: Session) -> UserDB | None:
    user_db = db.query(UserDB).filter(UserDB.email == email).first()

    if user_db is None:
        return None
    if verify_password(password, user_db.hashed_password):
        return user_db
    return None


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> UserDB:

    credentials_exception = HTTPException(
        status_code=401,
        detail="認証情報を確認できませんでした。",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        token = credentials.credentials
        payload = decode_access_token(token=token)
        subject = payload.get("sub")
        if subject is None:
            raise credentials_exception

        user_id = int(subject)
    except (InvalidTokenError, ValueError):
        raise credentials_exception

    user_db = db.query(UserDB).filter(UserDB.user_id == user_id).first()

    if user_db is None:
        raise credentials_exception
    return user_db


@router.post("/users", status_code=201, response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)) -> UserDB:
    try:
        hashed_password = hash_password(user.password)

        user_db = UserDB(email=str(user.email), hashed_password=hashed_password)

        db.add(user_db)
        db.commit()
        db.refresh(user_db)

        return user_db
    except IntegrityError as error:
        db.rollback()
        if (
            isinstance(error.orig, UniqueViolation)
            and error.orig.diag.constraint_name == "users_email_key"
        ):
            raise HTTPException(
                status_code=409,
                detail="同じメールアドレスのユーザーがすでに登録されています。",
            )
        logger.exception("ユーザーデータがDB制約に違反しました。")
        raise HTTPException(
            status_code=500, detail="ユーザーの登録処理中に失敗しました。"
        )
    except SQLAlchemyError:
        logger.exception("ユーザーの登録に失敗しました。")
        db.rollback()
        raise HTTPException(
            status_code=500, detail="ユーザーの登録処理中に失敗しました。"
        )


@router.post("/login", response_model=TokenResponse)
def login(login_data: UserLogin, db: Session = Depends(get_db)) -> TokenResponse:
    authenticated_user = authenticate_user(
        email=str(login_data.email),
        password=login_data.password,
        db=db,
    )

    if authenticated_user is None:
        raise HTTPException(
            status_code=401,
            headers={"WWW-Authenticate": "Bearer"},
            detail="メールアドレスまたはパスワードが正しくありません。",
        )
    access_token = create_access_token(subject=str(authenticated_user.user_id))

    response_token = TokenResponse(access_token=access_token, token_type="bearer")
    return response_token


@router.get("/users/me", response_model=UserResponse)
def read_current_user(current_user: UserDB = Depends(get_current_user)) -> UserDB:
    return current_user
