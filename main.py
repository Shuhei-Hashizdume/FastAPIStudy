from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.books import router as books_router
from routers.users import router as users_router

app = FastAPI()
allowed_origins = [
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=False,
    allow_methods=["GET", "POST", "PATCH", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)
app.include_router(books_router)
app.include_router(users_router)
