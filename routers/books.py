import logging
from fastapi import APIRouter, Depends, HTTPException, Query
from schemas import BookRequest, BookResponse, BookUpdate
from database import get_db
from sqlalchemy.orm import Session, joinedload, session
from models import BookDB, UserDB
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from psycopg.errors import UniqueViolation
from routers.users import get_current_user

logger = logging.getLogger(__name__)
router = APIRouter()


# 登録
def find_book_by_isbn(isbn: str, db: Session) -> BookDB | None:
    return db.query(BookDB).filter(BookDB.isbn == isbn).first()


@router.post("/books", status_code=201, response_model=BookResponse)
def add_book(
    book: BookRequest,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user),
):
    try:
        if book.isbn is not None:
            existing_book = find_book_by_isbn(isbn=book.isbn, db=db)
            if existing_book is not None:
                raise HTTPException(
                    status_code=409, detail="同じISBNの書籍がすでに登録されています。"
                )
        book_db = BookDB(
            title=book.title,
            author=book.author,
            isbn=book.isbn,
            owner_id=current_user.user_id,
        )

        db.add(book_db)
        db.commit()
        db.refresh(book_db)

        return book_db
    except IntegrityError as error:
        logger.exception("書籍データがDB制約に違反しました。")
        db.rollback()
        if (
            isinstance(error.orig, UniqueViolation)
            and error.orig.diag.constraint_name == "uq_books_isbn"
        ):
            raise HTTPException(
                status_code=409, detail="同じISBNの書籍がすでに登録されています。"
            )

        raise HTTPException(status_code=500, detail="書籍の登録処理中に失敗しました。")
    except SQLAlchemyError:
        logger.exception("書籍の登録に失敗しました。")
        db.rollback()
        raise HTTPException(status_code=500, detail="書籍の登録処理中に失敗しました。")


# 書籍一覧取得
@router.get("/books", response_model=list[BookResponse])
def show_books(
    author: str | None = None,
    offset: int = Query(default=0, ge=0),
    limit: int = Query(
        default=20,
        ge=1,
        le=100,
    ),
    db: Session = Depends(get_db),
):
    query = db.query(BookDB).options(joinedload(BookDB.publisher))

    if author is not None:
        query = query.filter(BookDB.author == author)
    books = query.order_by(BookDB.book_id).offset(offset).limit(limit).all()
    return books


# 条件による一部取得
@router.get("/books/{book_id}", response_model=BookResponse)
def show_book(book_id: int, db: Session = Depends(get_db)):

    book = db.query(BookDB).filter(BookDB.book_id == book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="該当する本がありません。")
    return book


# 一部更新
@router.patch("/books/{book_id}", response_model=BookResponse)
def update_book(
    book_id: int,
    book: BookUpdate,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user),
):
    try:
        target_book = db.query(BookDB).filter(BookDB.book_id == book_id).first()
        if target_book is None:
            raise HTTPException(status_code=404, detail="該当する本がありません。")
        if target_book.owner_id != current_user.user_id:
            raise HTTPException(
                status_code=403, detail="この書籍を変更する権限がありません。"
            )

        update_values = {}
        if book.isbn is not None:
            existing_book = db.query(BookDB).filter(BookDB.isbn == book.isbn).first()
            if (
                existing_book is not None
                and existing_book.book_id != target_book.book_id
            ):
                raise HTTPException(
                    status_code=409,
                    detail="同じISBNの書籍がすでに登録されています。",
                )
            update_values["isbn"] = book.isbn
        if book.title is not None:
            update_values["title"] = book.title
        if book.author is not None:
            update_values["author"] = book.author
        update_values["version"] = BookDB.version + 1

        updated_rows = (
            db.query(BookDB)
            .filter(BookDB.book_id == book_id, BookDB.version == book.version)
            .update(
                update_values,
                synchronize_session=False,
            )
        )
        if updated_rows == 0:
            db.rollback()
            raise HTTPException(
                status_code=409, detail="該当の書籍がすでに更新されています。"
            )
        db.commit()
        db.refresh(target_book)
        return target_book
    except HTTPException:
        raise
    except SQLAlchemyError:
        logger.exception("書籍の更新に失敗しました。")
        db.rollback()
        raise HTTPException(status_code=500, detail="書籍の更新処理中に失敗しました。")


# 削除
@router.delete("/books/{book_id}", status_code=204)
def delete_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user),
):
    try:
        target_book = db.query(BookDB).filter(BookDB.book_id == book_id).first()

        if target_book is None:
            raise HTTPException(status_code=404, detail="該当する本がありません。")
        if target_book.owner_id != current_user.user_id:
            raise HTTPException(
                status_code=403, detail="この書籍を削除する権限がありません。"
            )

        db.delete(target_book)
        db.commit()
    except HTTPException:
        raise
    except SQLAlchemyError:
        logger.exception("書籍の削除に失敗しました。")
        db.rollback()
        raise HTTPException(status_code=500, detail="書籍の削除処理中に失敗しました。")
