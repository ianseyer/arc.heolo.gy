from py2neo import Node, Relationship, Graph
import requests, json, sys

print "Performing pathfinding search with", sys.argv

if len(sys.argv) != 4:
    print "You failed to enter the correct arguments."
    print "article one, article two, depth"
else:
    graph = Graph("http://neo4j:wikipedia@localhost:7474/db/data/")

    a = graph.find_one("Article", "lowerTitle", sys.argv[1].lower())
    b = graph.find_one("Article", "lowerTitle", sys.argv[2].lower())
    if a and b:
        ENDPOINT = "http://neo4j:wikipedia@localhost:7474/db/data/"
        request = {
            "to":ENDPOINT+"node/"+str(b._id),
            "max_depth": int(sys.argv[3]),
            "relationships": {
                "type":"LINKS",
                "direction":"out"
            },
            "algorithm":"allPaths"
        }
        r = requests.post(ENDPOINT+"node/"+str(a._id)+"/paths", data=json.dumps(request))
        # print r.json()
        if r.status_code == 200:
            for path in r.json():
                print "Path:"
                for node in path['nodes']:
                    # print node
                    retrieved_node = graph.node(node.split('/node/')[1])
                    print retrieved_node.properties['title'], "->"
                print "--------------------"
        else:
            print "Something went wrong."
            print sys.exc_info()[0]

    else:
        if not a:
            print sys.argv[1], "not found!"
        else:
            print sys.argv[2], "not found!"
