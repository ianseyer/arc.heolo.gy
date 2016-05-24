from pymongo import MongoClient
from bs4 import BeautifulSoup
import os, sys

rootdir = '/home/relay/code/wiki/dump/'
mongo = MongoClient() #default local
db = mongo.wiki

def build_db(file):
    '''
    Iterate through each extracted wiki file xml to extract relational data
    '''
    collection = BeautifulSoup(file, 'lxml')
    #remove style and div tags
    if collection.div:
        collection.div.decompose()
    if collection.style:
        collection.style.decompose()

    for entry in collection.find_all('doc'):
        #first, extract all relations by title
        relations = []
        try:
            for link in entry.find_all('a'):
                relations.append(link['href'])
        except:
            print 'Error parsing', entry['title']

        document = {
            'title':entry['title'],
            'url':entry['url'],
            'raw':entry.text,
            'relations':relations
        }

        try:
            db.entries.insert_one(document)
            print document['title']
        except AttributeError as e:
            print e
        except:
            print 'could not insert', entry['title']
            print sys.exc_info()[0]

for subdir, dirs, files in os.walk(rootdir):
    #iterate through our dump directory
    for file in files:
        #build the database entries
        build_db(open(subdir+'/'+file))
