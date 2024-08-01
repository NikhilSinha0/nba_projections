package main

import (
	"encoding/csv"
	"fmt"
	"os"
	"path/filepath"
	"strings"

	"github.com/gocolly/colly"
)

const (
	BASE_URL = "https://basketball.realgm.com/ncaa/stats/%d/Averages/Qualified/All/Season/All/points/desc/%d"
)

func main() {

	var out [][]string
	rows := []string{"Num", "PlayerID", "Player", "Conference", "Team", "GP", "MPG", "PPG", "FGM", "FGA", "FG%", "3PM", "3PA", "3P%", "FTM", "FTA", "FT%", "ORB", "DRB", "RPG", "APG", "SPG", "BPG", "TOV", "PF", "Year"}
	out = append(out, rows)

	for i := 2003; i < 2025; i++ {
		c := colly.NewCollector()
		j := 1
		init_link := fmt.Sprintf(BASE_URL, i, j)

		c.OnRequest(func(r *colly.Request) {
			fmt.Println("Visiting:", r.URL)
		})

		c.OnHTML("tbody>tr", func(e *colly.HTMLElement) {
			var sub []string
			e.ForEach("td", func(k int, d *colly.HTMLElement) {
				d.ForEach("a", func(k1 int, d1 *colly.HTMLElement) {
					href := d1.Attr("href")
					parts := strings.Split(href, "/")
					if parts[1] == "player" {
						sub = append(sub, strings.Join([]string{parts[2], parts[4]}, "-"))
					} else {
						sub = append(sub, parts[3])
					}
				})
				sub = append(sub, d.Text)
			})
			sub = append(sub, fmt.Sprintf("%d", i))
			out = append(out, sub)
		})

		c.OnHTML("p>a", func(e *colly.HTMLElement) {
			if e.Text == "Next Page »" {
				j += 1
				e.Request.Visit(fmt.Sprintf(BASE_URL, i, j))
			}
		})

		c.Visit(init_link)
	}

	exec, err := os.Executable()
	if err != nil {
		printAndExit("Failed to get executable path", err)
	}
	dataPath := filepath.Join(filepath.Dir(filepath.Dir(filepath.Dir(exec))), "data")

	f, err := os.Create(filepath.Join(dataPath, "college_stats.csv"))
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
