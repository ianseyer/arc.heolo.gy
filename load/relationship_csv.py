from py2neo import Graph, Node, Relationship
from py2neo.packages.httpstream import http
import math, json

http.socket_timeout = 9999

graph = Graph("http://neo4j:wikipedia@localhost:7474/db/data")

import csv
with open('relationships.csv', 'wb') as file:
	writer = csv.DictWriter(file, fieldnames=["TYPE","START_ID","END_ID"])
	writer.writeheader()
	print graph.cypher.execute("MATCH (n) RETURN COUNT(n)")[0][0]
	size = int(graph.cypher.execute("MATCH (n) RETURN COUNT(n)")[0][0])
	batch_size = 1000
	num_batches = int(math.ceil(size/batch_size))
	for batch_number in range(num_batches):
		batch = graph.cypher.execute("MATCH (n) RETURN n SKIP "+str(batch_size*batch_number) + " LIMIT " + str(batch_size))
		for n in batch:
			n = n[0]
			print n.properties['title']
			print json.dumps(n.properties['relations'])
			for r in n.properties['relations'][1:-1].split(','):
				data = {}
				data['TYPE'] = 'LINKS'
				data['START_ID'] = n._id
				print r
				try:
					relating_node = graph.cypher.execute_one('MATCH (n:Article {lowerTitle: "'+r+'"}) RETURN n LIMIT 1')
					if relating_node:
						data['END_ID'] = relating_node._id
						print data
						writer.writerow(data)
			