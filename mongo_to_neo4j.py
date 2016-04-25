from pymongo import MongoClient
from py2neo import Graph, Node, Relationship
import os, sys, urllib
'''
This file loads our mongo database into a neo4j graphDb.
'''

mongo = MongoClient() #default local mongo

wikipedia = mongo.wiki.entries

graph = Graph("https://neo4j:wikipedia@localhost:7473/db/data/")
#short of doing a recursive network expansion of creation,
#we will have to iterate twice through the mongo db:
#first to create all the entry Nodes
#and second to create all their relations

def create_nodes():
    for entry in wikipedia.find():
        #iterate through all of our entries, and build a neo4j node for each entry
        try:
            print "inserting", entry['title']
            # COUNT+=1
            graph.create(
                Node("Article",
                    title=entry['title'].lower(),
                    raw=entry['raw'],
                    url=entry['url'],
                    mongo_id=str(entry['_id'])
                )
            )
        except UnboundLocalError as e:
            print "failed to commit", entry['title']
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
    count = 0
    for entry in wikipedia.find():
        #iterate through all entries again, and build a relationship between parent and relations
        parent = graph.find_one("Article", "title", entry['title'].lower())
        for relation in entry['relations']:
            try:
                print relation
                print 'creating relationship between',entry['title'],'and',urllib.unquote(relation).lower().encode('utf-8')
                child = graph.find_one("Article", "title", urllib.unquote(relation).lower().encode('utf-8'))
                #be sure to use the unique restraint
                if parent and child:
                    if Relationship(parent, "LINKS", child).exists():
                        print "Relationship already exists!"
                    else:
                        graph.create_unique(
                            Relationship(
                                parent,
                                "LINKS",
                                child
                            )
                        )
                        count+=1
                        print count
                else:
                    print "Relating article not found"
            except:
                print "Unable to create relationship between", entry['title'], "and", relation
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
