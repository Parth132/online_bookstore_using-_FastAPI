from typing import Optional, List, Annotated
from fastapi import FastAPI, Path, Query, Depends
from pydantic import BaseModel
import models
from datetime import datetime
from database import engine, SessionLocal
from sqlalchemy.orm import Session
import books,ratings
import uvicorn

app = FastAPI(
    title="FastAPI",
    description="Description",
)
models.Base.metadata.create_all(bind = engine)

app.include_router(books.router)
app.include_router(ratings.router)

if __name__ == "__main__":
    uvicorn.run(app)