from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date
from database import Base
from sqlalchemy.orm import relationship

class Books(Base):
	__tablename__ = "books"
	id = Column(Integer, primary_key = True, index = True)
	title = Column(String, index = True)
	author = Column(String, index = True)
	published_date = Column(Date, index = True)
	ISBN_number = Column(String(13), index = True)
	price = Column(Integer, index = True)

	rating = relationship("Ratings", back_populates='book')

class Ratings(Base):
	__tablename__ = "ratings"
	id = Column(Integer, primary_key = True, index = True)
	book_id = Column(Integer, ForeignKey("books.id"))
	user_name = Column(String, index = True)
	rating = Column(Integer, index = True)
	review_text = Column(String, index = True)

	book = relationship('Books', back_populates = 'rating')