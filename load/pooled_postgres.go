package main

import (
	"github.com/jinzhu/gorm"
	_ "github.com/jinzhu/gorm/dialects/postgres"
	"os"
	"fmt"
	"runtime"
	"path/filepath"
	_ "database/sql"
	_ "github.com/lib/pq"
	"github.com/PuerkitoBio/goquery"
	"github.com/jeffail/tunny"
	"github.com/jmoiron/sqlx/types"
	"encoding/json"
)

//our Article definition
type Article struct {
	gorm.Model
	Title string `gorm:"not null;unique"`
	Url string
	Raw string `sql:"text"`
	Relations types.JSONText
	Filename string
}

var db *gorm.DB

func insertFileIntoDB(file string) int {
	fmt.Println(file)
	open, err := os.Open(file)
	if err == nil {
		doc, err := goquery.NewDocumentFromReader(open)
		if err == nil {
			fmt.Println("HEO")
			count := 0
			doc.Find("doc").Each(func(i int, entry *goquery.Selection) {
				relations := []string{}
				entry.Find("a").Each(func(i int, reference *goquery.Selection) {
					relations = append(relations, reference.Text())
				})
				title, _ := entry.Attr("title")
				url, _ := entry.Attr("url")
				jsonRelations, _ := json.Marshal(relations)
				article := Article{Title: title, Url: url, Raw: entry.Text(), Relations: jsonRelations, Filename:file}
				db.Create(&article)
				count = count + 1
			})
			fmt.Println("success")
			open.Close()
			return count
		}
		fmt.Println(err)
		return 0
	}
	fmt.Println(err)
	return 0
}

func main() {
	//connect to our database
	db, _ = gorm.Open("postgres", "postgres://relay:relay@localhost:5432/wikipedia")
	dumpDir := "/home/relay/code/wiki/arc.heolo.gy/dump/"
	fileList := []string{}
	err := filepath.Walk(dumpDir, func(path string, f os.FileInfo, err error) error {
		fileList = append(fileList, path)
		return nil
	})
	fmt.Println(err)
	runtime.GOMAXPROCS(runtime.NumCPU())
	numCPUs := runtime.NumCPU()
	fmt.Println(len(fileList))	
	pool, _ := tunny.CreatePool(numCPUs, func(object interface{}) interface{} {
        	// Do something that takes a lot of work
		status := insertFileIntoDB(object.(string))
        	return status
	}).Open()

	defer pool.Close()

	for _, file := range fileList[1000:] {
		pool.SendWork(file)
	}
}

