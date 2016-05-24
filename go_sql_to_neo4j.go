package main

import ( 
	"fmt"
	"database/sql"
	"strings"
	_ "gopkg.in/cq.v1"
)

func build_relationships(g sql.DB, entry struct{}) int {
	fmt.Println(entry)
	neo_query, err := g.Prepare(`
			match (n:Article)
			where n.lowerTitle = {0}
			return n
			limit 1`)
	if(err != nil){
		fmt.Println(err)
	}
	defer neo_query.Close()

	parent, err := neo_query.Query(strings.ToLower(entry.title))
	if(err != nil){
		fmt.Println(err)
	}
	defer parent.Close()
	
	var node string
	err := fmt.Println(parent.Scan(&node))
	if(err != nil){
		fmt.Println(err)
	}
	return 1
}

func main() {
	db, err := sql.Open("postgres://relay:relay@localhost:5432/wikipedia")
	if(err != nil ){
		fmt.Println(err)
	}
	g, err := sql.Open("http://neo4j:wikipedia@localhost:7474")
	if(err != nil ){
		fmt.Println(err)
	}
	defer db.Close()
	defer g.Close()
	
	for _, entry := db.Limit(10).Find(&articles) {
		go build_relationships(g, entry)
	}
}
