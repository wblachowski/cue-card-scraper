# Cue Cards Scraper

Python script for scraping cue cards from www.ielts-mentor.com website. Cue cards are used as a speaking test at exams such as IELTS or C2 Proficiency. Each card asks the candidate to speak about a given topic for 2 minutes.

## Usage

```bash
$ py cards_scraper.py -l <limit> -o <output file>
```

## Options

```
--help -h               Show help message and exit.

--limit  -l             Upper limit on the number of cards to download.
                        Default: 1000

--output  -o            Output file. Has to be ither a text file (*.txt) or an SQLite database file (*.db).
                        Default: output.txt
```
