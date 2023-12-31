from typing import Optional, List, Annotated
from fastapi import FastAPI, Path, Query, Depends, APIRouter, HTTPException
from pydantic import BaseModel
import models
from datetime import datetime
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy import func, desc

router = APIRouter()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]


class BooksBase(BaseModel):
    title: str
    author: str
    published_date: datetime
    ISBN_number: str
    price: int

@router.get("/books")
async def get_all_books(db: db_dependency):
    result = db.query(models.Books).all()
    if not result:
        raise HTTPException(status_code=404, detail='No books found')
    return result

@router.get("/books/rated")
async def get_books_by_ratings(db: db_dependency):
    details = db.query(
    models.Books,
    func.avg(models.Ratings.rating).label("avg_rating"),
).join(models.Ratings, models.Books.id == models.Ratings.book_id).group_by(models.Books.id).order_by(desc("avg_rating")).all()
    if not details:
        raise HTTPException(status_code=404, detail='No books found')
    result = []
    print(details)
    for book in details:
        temp = book[0].__dict__
        temp['average_rating'] = book[1]
        result.append(temp)
    return result

@router.get("/books/{id}")
async def get_book_by_id(book_id: int, db: db_dependency):
    result = db.query(models.Books).filter(models.Books.id == book_id).all()
    if not result:
        raise HTTPException(status_code=404, detail='Book is not found!')
    return result

@router.put("/books/{id}")
async def update_book_details(book_id: int, book: BooksBase, db: db_dependency):
    result = db.query(models.Books).filter(models.Books.id == book_id).first()
    if not result:
        raise HTTPException(status_code=404, detail='Book not found')
    result.title = book.title
    result.author = book.author
    result.published_date = book.published_date
    result.ISBN_number = book.ISBN_number
    result.price = book.price
    db.commit()
    db.refresh(result)
    return {'message':'details updated successfully'}

@router.delete("/books/{id}")
async def delete_book(book_id: int, db: db_dependency):
    result = db.query(models.Books).filter(models.Books.id == book_id).first()
    if not result:
        raise HTTPException(status_code=404, detail='Book not found')
    db.delete(result)
    db.commit()
    return {'message':'book deleted successfully'}

@router.post("/books")
async def add_books(book: BooksBase, db: db_dependency):
    db_book = models.Books(title = book.title, author = book.author, 
        published_date = book.published_date, ISBN_number = book.ISBN_number, price = book.price)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return {'message':'book added successfully'}