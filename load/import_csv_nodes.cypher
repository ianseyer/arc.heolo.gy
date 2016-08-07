USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM "file:///formatted.csv" AS row
CREATE (:Article {title: row.title, url: row.url, text:row.raw, filename: row.filename, pgID: row.id});
