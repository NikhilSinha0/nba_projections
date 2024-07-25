package main

import (
	"fmt"

	"github.com/gocolly/colly"
)

const (
	BASE_URL = "https://basketball.realgm.com/ncaa/stats/%d/Averages/Qualified/All/Season/All/points/desc/%d"
)

func main() {
	c := colly.NewCollector()

	// var out []string

	for i := 2003; i < 2025; i++ {
		j := 1
		init_link := fmt.Sprintf(BASE_URL, i, j)

		var sub []string

		c.OnRequest(func(r *colly.Request) {
			fmt.Println("Visiting:", r.URL)
		})

		c.OnHTML("tbody>tr", func(e *colly.HTMLElement) {
			e.ForEach("td", func(k int, d *colly.HTMLElement) {
				sub = append(sub, d.Text)
			})
		})

		c.OnHTML("p>a", func(e *colly.HTMLElement) {
			if e.Text == "Next Page »" {
				j += 1
				e.Request.Visit(fmt.Sprintf(BASE_URL, i, j))
			}
		})

		c.Visit(init_link)
	}
}
