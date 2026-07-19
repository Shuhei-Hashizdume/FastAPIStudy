from fastapi import APIRouter, Depends, HTTPException
from schemas import BookRequest, BookResponse, BookUpdate
from database import get_db
from sqlalchemy.orm import Session
from models import BookDB

router = APIRouter()


# 登録
@router.post("/books", status_code=201, response_model=BookResponse)
def add_book(book: BookRequest, db: Session = Depends(get_db)):
    try:
        book_db = BookDB(title=book.title, author=book.author)

        db.add(book_db)
        db.commit()
        db.refresh(book_db)

        return book_db
    except Exception:
        db.rollback()
        raise


# 全部取得
@router.get("/books", response_model=list[BookResponse])
def show_books(author: str | None = None, db: Session = Depends(get_db)):
    if author is None:
        books = db.query(BookDB).all()
    else:
        books = db.query(BookDB).filter(BookDB.author == author).all()
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
def update_book(book_id: int, book: BookUpdate, db: Session = Depends(get_db)):
    try:
        target_book = db.query(BookDB).filter(BookDB.book_id == book_id).first()
        if target_book is None:
            raise HTTPException(status_code=404, detail="該当する本がありません。")
        if book.title is not None:
            target_book.title = book.title
        if book.author is not None:
            target_book.author = book.author
        db.commit()
        db.refresh(target_book)
        return target_book
    except Exception:
        db.rollback()
        raise


# 削除
@router.delete("/books/{book_id}", status_code=204)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    try:
        target_book = db.query(BookDB).filter(BookDB.book_id == book_id).first()

        if target_book is None:
            raise HTTPException(status_code=404, detail="該当する本がありません。")

        db.delete(target_book)
        db.commit()
    except Exception:
        db.rollback()
        raise
