from fastapi import FastAPI , HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, query, session
from sqlalchemy import Integer,String,Column
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from fastapi import Depends

def get_db():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()    

app = FastAPI()
engine = create_engine("sqlite:///book.db")
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class BookRequest(BaseModel):
    title:str
    author:str

class BookUpdate(BaseModel):
    title:str |  None = None
    author:str |  None = None

class BookDB(Base):
    __tablename__ = "books"
    book_id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)    

Base.metadata.create_all(bind=engine)

#SQLite版　　API 登録
@app.post("/books",status_code=201)
def add_book(book: BookRequest, db: Session = Depends(get_db)):
    try:
        book_db = BookDB(
            title = book.title,
            author = book.author
        )
        
        db.add(book_db)
        db.commit()
        db.refresh(book_db)

        return {
            "message":"本が追加されました！",
            "book":book_db
        }
    except Exception:
        db.rollback()
        raise       

#SQLite版　　API 取得　全件もしくは著者取得
@app.get("/books")
def show_books(author: str | None = None, db: Session = Depends(get_db)):
    if author is None:
        books = db.query(BookDB).all()
    else:
        books = (
            db.query(BookDB)
            .filter(BookDB.author == author)
            .all()
        )
    return books
         

#SQLite版　　API 条件取得 
@app.get("/books/{book_id}")
def show_book(book_id:int,db: Session = Depends(get_db)):
    
    book = (
        db.query(BookDB)
        .filter(BookDB.book_id == book_id)
        .first()
    )
    if book is None:
        raise HTTPException(
            status_code=404,
            detail="該当する本がありません。"
        )        
    return book


#SQLite版　　API 更新
@app.patch("/books/{book_id}")
def update_book(book_id :int, book : BookUpdate, db: Session = Depends(get_db)):
    try:
        target_book = (
            db.query(BookDB)
            .filter(BookDB.book_id == book_id)
            .first()
            )
        if target_book is None:
            raise HTTPException(
                status_code=404,
                detail="該当する本がありません。"
            )
        if book.title is not None:    
            target_book.title = book.title
        if book.author is not None:    
            target_book.author = book.author
        db.commit()
        db.refresh(target_book)
        return {
            "message" : "更新しました。",
            "book":target_book}
    except Exception:
        db.rollback()
        raise   
   

#SQLite版　　API 削除
@app.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    try:
        target_book = (
            db.query(BookDB)
            .filter(BookDB.book_id == book_id)
            .first()
            )

        if target_book is None:
            raise HTTPException(
                status_code=404,
                detail="該当する本がありません。"
            )

        db.delete(target_book)
        db.commit()    
        return {"message":"削除されました"}
    except Exception:
        db.rollback()
        raise    
