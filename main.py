from fastapi import FastAPI
from database import Base, engine
from routers.books import router as books_router

app = FastAPI()
app.include_router(books_router)

Base.metadata.create_all(bind=engine)
