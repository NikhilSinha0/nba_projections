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
	BASE_URL        = "https://basketball.realgm.com/ncaa/stats/%d/Averages/Qualified/All/Season/All/points/desc/%d"
	PLAYER_BASE_URL = "https://basketball.realgm.com/player/%s/Summary/%s"
)

func main() {
	playerYearMap := map[string]string{}
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
						playerID := strings.Join([]string{parts[2], parts[4]}, "-")
						sub = append(sub, playerID)
						playerYearMap[playerID] = fmt.Sprintf(PLAYER_BASE_URL, parts[2], parts[4])
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

	// This is slow and I hate it but it works
	// Basically visit every player's page and pull their birth year. For the full amount it takes ~2 hours

	var players [][]string
	playerRows := []string{"PlayerID", "BirthYear"}
	players = append(players, playerRows)
	total := len(playerYearMap)
	i := 1

	for pid, link := range playerYearMap {
		c := colly.NewCollector()

		c.OnRequest(func(r *colly.Request) {
			fmt.Printf("Visiting link %d of %d\n", i, total)
			i += 1
		})

		c.OnHTML("p>a", func(e *colly.HTMLElement) {
			href := e.Attr("href")
			if strings.HasPrefix(href, "/info/birthdays") {
				players = append(players, []string{pid, strings.TrimSpace(strings.Split(e.Text, ",")[1])})
			}
		})

		c.Visit(link)
	}

	f1, err := os.Create(filepath.Join(dataPath, "college_birthyears.csv"))
	if err != nil {
		printAndExit("Failed to create college birth years file", err)
	}
	w1 := csv.NewWriter(f1)
	for _, record := range players {
		if err := w1.Write(record); err != nil {
			printAndExit("Failed to write record to college birth years file", err)
		}
	}

	w1.Flush()

	if err := w1.Error(); err != nil {
		printAndExit("Failed to completely write college birth years file", err)
	}
}

func printAndExit(msg string, err error) {
	fmt.Println(msg)
	fmt.Println(err)
	os.Exit(1)
}
