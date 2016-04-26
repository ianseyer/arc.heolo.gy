from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.dialects.postgresql import JSON, TEXT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pymongo import MongoClient
from bs4 import BeautifulSoup
from tidylib import tidy_document

import os, sys, json

rootdir = '/home/relay/code/wiki/dump/'

Base = declarative_base()

engine = create_engine("postgres://relay:relay@localhost:5432/wikipedia", echo=False)
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()
connection = engine.connect()


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


articles = Article.__table__
insert = articles.insert()


def build_db(file):
    """
    This populates our database. Relations will be stored as a JSON list
    """

    collection = BeautifulSoup(file, 'lxml')

    #tidy up our XML, removing all div tags
    for div in collection.find_all('div'):
        div.replaceWith('')

    #remove style and div tags
    if collection.div:
        collection.div.decompose()
    if collection.style:
        collection.style.decompose()

    articles_in_file = []
    for entry in collection.find_all('doc'):
        relations = []
        try:
            for link in entry.find_all('a'):
                relations.append(link['href'])
        except:
            print "Error Parsing", entry['title']

        articles_in_file.append(
            Article(
                title=entry['title'],
                url=entry['url'],
                raw=entry.text,
                relations=json.dumps(relations),
                filename=file.name
            )
        )

    try:
        session.bulk_save_objects(articles_in_file)
        session.commit()
        print "inserted", len(articles_in_file), "articles"

    except Exception as e:
        session.rollback()
        print e

if __name__ == '__main__':
    for subdir, dirs, files in os.walk(rootdir):
    #iterate through our dump directory
        for file in files:
            #build the database entries
            build_db(open(subdir+'/'+file))
