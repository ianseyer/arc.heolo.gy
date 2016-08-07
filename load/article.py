from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.dialects.postgresql import JSON, TEXT

Base = declarative_base()


class Article(Base):
    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True)
    url = Column(String)
    raw = Column(TEXT)
    relations = Column(JSON)
    filename = Column(String) #which file the article is located in

    def __repr__(self):
        return self.title, self.url

