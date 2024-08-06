package main

import (
	"encoding/csv"
	"fmt"
	"os"
	"path/filepath"
	"slices"
	"strings"

	"github.com/gocolly/colly"
)

const (
	BASE_URL = "https://www.sports-reference.com/cbb/awards/men/rsci-recruit-rankings-%d.html"
)

func main() {

	var out [][]string
	rows := []string{"Rank", "Player", "Schools", "Year"}
	out = append(out, rows)

	vals := []string{"rank", "player", "schools"}

	for i := 1998; i < 2024; i++ {
		c := colly.NewCollector()
		init_link := fmt.Sprintf(BASE_URL, i)

		c.OnRequest(func(r *colly.Request) {
			fmt.Println("Visiting:", r.URL)
		})

		c.OnHTML("tbody>tr:not(.thead)", func(e *colly.HTMLElement) {
			var sub []string
			e.ForEach("th", func(k int, d *colly.HTMLElement) {
				stat := d.Attr("data-stat")
				if slices.Contains(vals, stat) {
					sub = append(sub, strings.TrimPrefix(d.Text, "T"))
				}
			})
			e.ForEach("td", func(k int, d *colly.HTMLElement) {
				stat := d.Attr("data-stat")
				if slices.Contains(vals, stat) {
					sub = append(sub, d.Text)
				}
			})
			sub = append(sub, fmt.Sprintf("%d", i))
			out = append(out, sub)
		})
		c.Visit(init_link)
	}

	exec, err := os.Executable()
	if err != nil {
		printAndExit("Failed to get executable path", err)
	}
	dataPath := filepath.Join(filepath.Dir(filepath.Dir(filepath.Dir(exec))), "data")

	f, err := os.Create(filepath.Join(dataPath, "hs_rankings.csv"))
	if err != nil {
		printAndExit("Failed to create college stats file", err)
	}
	w := csv.NewWriter(f)
	for _, record := range out {
		if err := w.Write(record); err != nil {
			printAndExit("Failed to write record to college stats file", err)
		}
	}

	w.Flush()

	if err := w.Error(); err != nil {
		printAndExit("Failed to completely write college stats file", err)
	}
}

func printAndExit(msg string, err error) {
	fmt.Println(msg)
	fmt.Println(err)
	os.Exit(1)
}
