MATCH (n:Article)
UNWIND split(substring(n.relations, 1, size(n.relations) -1), ',') as rel
MATCH (k:Article {lowerTitle: rel})
CREATE UNIQUE (n) -[r:LINKS]-> (k)
