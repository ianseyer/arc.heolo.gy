package main

import (
	"github.com/jinzhu/gorm"
	_ "github.com/jinzhu/gorm/dialects/postgres"
	"os"
	"fmt"
	"runtime/debug"
	"runtime"
	"path/filepath"
	_ "database/sql"
	_ "github.com/lib/pq"
	"github.com/PuerkitoBio/goquery"
)

//our Article definition
type Article struct {
	gorm.Model
	Title string `gorm:"not null;unique"`
	Url string
	Raw string `sql:"text"`
	Relations string
	Filename string
}

var db *gorm.DB

func insertFileIntoDB(file string) int {
	open, err := os.Open(file)
	if err == nil {
		doc, err := goquery.NewDocumentFromReader(open)
		if err == nil {
			fmt.Println("HEO")
			count := 0
			doc.Find("doc").Each(func(i int, entry *goquery.Selection) {
				relations := ""
				entry.Find("a").Each(func(i int, reference *goquery.Selection) {
					relations += reference.Text() + "::"
				})
				fmt.Println(len(relations))
				title, _ := entry.Attr("title")
				url, _ := entry.Attr("url")
				article := Article{Title: title, Url: url, Raw: entry.Text(), Relations: relations, Filename:file}
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
	runtime.GOMAXPROCS(runtime.NumCPU())
	debug.FreeOSMemory()
	//connect to our database
	db, _ = gorm.Open("postgres", "postgres://relay:relay@localhost:5432/wikipedia")
	//update our schema
	//db.Set("gorm:table_options", "ENGINE=postgres").AutoMigrate(&Article{})
	dumpDir := "/home/relay/code/wiki/arc.heolo.gy/dump/"
	fileList := []string{}
	err := filepath.Walk(dumpDir, func(path string, f os.FileInfo, err error) error {
		fileList = append(fileList, path)
		return nil
	})
	if err != nil {
		fmt.Println(err)
	}

	for idx, file := range fileList[:20] {
		fmt.Println(idx)
		go insertFileIntoDB(file)
	}
}

