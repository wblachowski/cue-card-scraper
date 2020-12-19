# Cue Cards Scraper

Python script for scraping cue cards from www.ielts-mentor.com website. Cue cards are used as a speaking test at exams such as IELTS or C2 Proficiency. Each card contains a question on a given topic, along with a few hints on what the candidate should include in their answer.

## Usage

```bash
$ py cards_scraper.py -l <limit> -o <output file>
```

Card are saved either to a text file or to a SQLite database, depending on the name of the output file.
Text output contains cue cards details separated by an empty line, for instance:

```
Describe a website that you bought something from.
You should say:
	what the website is
	what you bought from this website
	how satisfied you were with what you bought
and explain what you liked or disliked about using this website.

Describe a volunteer work experience you have had.
You should say:
	what volunteer work it was
	where it was
	why you volunteered
and explain how you felt about it.
```

If the output is a database file, the cards are saved to the `cards` table, with the following structure:

```

             title                   prompt                          bullets                                   ending
 ------------------------------ ----------------- --------------------------------------------- ------------------------------------
  Describe a website that you    You should say:   what the website is                           and explain what you liked or
  bought something from                            what you bought from this website             disliked about using this website.
                                                   how satisfied you were with what you bought
```

## Options

```
--help -h               Show help message and exit.

--limit  -l             Upper limit on the number of cards to download.
                        Default: 1000

--output  -o            Output file. Has to be ither a text file (*.txt) or an SQLite database file (*.db).
                        Default: output.txt
```
