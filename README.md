# iCoolScrapped

A simple scraper for iCoolHunt.com - based on Scrapy: http://www.scrapy.org

It scrapes data from the explore page and from the prey details  page.

It will scrape an arbitrary number of preys even if results are paginated by 20

## Usage
```bash
scrapy crawl icoolhunt -o icoolhunt.json -t json -a maxpreys=30
```

## Requirements

  * Python 2.7 1.9+
  * Scrapy 2.22
