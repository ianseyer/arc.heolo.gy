from py2neo import Node, Relationship, Graph
import requests, json, sys, urllib

g = Graph("http://neo4j:wikipedia@localhost:7474/db/data")

def pathfinder(one, two, depth=3):
    if not (one and two):
        raise "You must enter two search queries"

    one = urllib.unquote(one).lower().encode('utf-8') #sanitize
    two = urllib.unquote(two).lower().encode('utf-8') #sanitize

    print one, two
    #find our articles
    article_one = g.find_one("Article", "title", one)
    article_two = g.find_one("Article", "title", two)

    if not (article_one and article_two):
        print "Article not found!"
        return False

    #execute our path query
    ENDPOINT = "http://neo4j:wikipedia@localhost:7474/db/data/"
    request = {
        "to":ENDPOINT+"node/"+str(article_two._id),
        "max_depth": depth,
        "relations": {
            "type":"LINKS",
            "direction":"out"
        },
        "algorithm":"shortestPath"
    }

    r = requests.post(ENDPOINT+"node/"+str(article_one._id)+"/paths", data=json.dumps(request))

    if r.status_code != 200:
        print "Error finding paths!"
        return False

    print r.json()

    routes = r.json()

    for path in routes:
        for index, node in enumerate(path['nodes']):
            title = g.node(node.split('/node/')[1]).properties['title']
            path['nodes'][index] = title

    return routes
