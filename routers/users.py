import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas import UserCreate, UserResponse
from security import hash_password
from models import UserDB
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from psycopg.errors import UniqueViolation

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/users", status_code=201, response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
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
