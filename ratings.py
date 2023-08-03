from typing import Optional, List, Annotated
from fastapi import FastAPI, Path, Query, Depends, APIRouter, HTTPException
from pydantic import BaseModel
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
class RatingsBase(BaseModel):
    book_id: int
    user_name: str
    rating: int
    review_text: str

@router.post("/ratings")
async def add_new_rating(review: RatingsBase, db: db_dependency):
    if not(1 <= review.rating <= 5):
        raise HTTPException(status_code=400, detail='Invalid Rating')
    try:
        db_rating = models.Ratings(book_id = review.book_id, user_name = review.user_name, 
            rating = review.rating, review_text = review.review_text)
        db.add(db_rating)
        db.commit()
        db.refresh(db_rating)
        return {"message":"Rating added successfully"}
    except:
        raise HTTPException(status_code=404, detail='Invalid Book id')

@router.get("/ratings/{book_id}")
async def all_ratings_of_book_id(book_id:int, db: db_dependency):
    result = db.query(models.Ratings).filter(models.Ratings.book_id == book_id).all()
    if not result:
        raise HTTPException(status_code=404, detail='Book is not found!')
    return result
