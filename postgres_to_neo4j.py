from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.dialects.postgresql import JSON, TEXT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from py2neo import Graph, Node, Relationship
from bs4 import BeautifulSoup
from load_postgres import Article
import os, sys, json, urllib

rootdir = '/home/relay/code/wiki/dump/'

engine = create_engine("postgres://relay:relay@localhost:5432/wikipedia", echo=False)
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()
connection = engine.connect()

graph = Graph("http://neo4j:wikipedia@localhost:7474/db/data/")
#short of doing a recursive network expansion of creation,
#we will have to iterate twice through the db:
#first to create all the entry Nodes
#and second to create all their relations

def create_nodes():
    for entry in session.query(Article).yield_per(1000):
        #iterate through all of our entries, and build a neo4j node for each entry
        try:
            print "inserting", entry.title
            # COUNT+=1
            graph.create(
                Node("Article",
                    title=entry.title.lower(),
                    raw=entry.raw,
                    url=entry.url,
                    filename=entry.filename
                )
            )
        except UnboundLocalError as e:
            print "failed to commit", entry.title
            print e
        except TypeError as e:
            print e
        except SystemError as e:
            print e
        except Exception as e:
            print e
        except:
            print "failed to commit", entry['title']
            print sys.exc_info()[0]


def create_relationships():
    for entry in session.query(Article).yield_per(5000):
        #iterate through all entries again, and build a relationship between parent and relations
        parent = graph.find_one("Article", "title", entry.title.lower())
        for relation in json.loads(entry.relations):
            try:
                child = graph.find_one("Article", "title", urllib.unquote(relation).lower().encode('utf-8'))
                #be sure to use the unique restraint
                if parent and child:
                    graph.create_unique(
                        Relationship(
                            parent,
                            "LINKS",
                            child
                        )
                    )
                else:
                    print "Relating article not found"
            except Exception as e:
                print e
                print "Unable to create relationship between", entry.title, "and", relation
                print sys.exc_info()[0]
        # count+=1
        # print count,"/",wiki_count

if __name__ == '__main__':
    # COUNT=0
    # print "Creating nodes."
    # create_nodes()
    # print "Successfully inserted", COUNT, "articles."
    print "Building relationships."
    create_relationships()
