# PyWebScraper

A Python project that scrapes job postings from [Y Combinator Jobs](https://www.ycombinator.com/jobs) and presents them in a web interface.

## Features

- Scrapes jobs and stores them in `jobs.json`.
- Displays listings in a **paginated HTML table** using Flask.
- Table columns are **sortable**.
- Raw JSON API available at `/rawjson`.
- Avoids duplicates using hashing.

## Libraries Used

Python, Requests, BeautifulSoup, Hashlib, Flask, HTML/CSS, JavaScript
