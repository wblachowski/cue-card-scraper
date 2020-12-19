import asyncio
import aiohttp
import sqlite3
import argparse
import sys
import os
from pyquery import PyQuery

BASE_URL = 'https://www.ielts-mentor.com'
CARDS_URL = BASE_URL + '/cue-card-sample'

parser = argparse.ArgumentParser()
parser.add_argument('-l', '--limit', type=int, default=1000,
                    help='upper limit of cards to download')
parser.add_argument('-o', '--output', default='output.txt',
                    help='output file')


class Cue:
    def __init__(self, title, prompt, bullets, ending):
        self.title = title
        self.prompt = prompt
        self.bullets = bullets
        self.ending = ending

    def __str__(self):
        bullets = '\n'.join(f'\t{b}' for b in self.bullets)
        return (f"{self.title}\n"
                f"{self.prompt}\n"
                f"{bullets}\n"
                f"{self.ending}")

    @staticmethod
    def from_markup(markup):
        pq = PyQuery(markup)
        title = pq(pq("article span:first-of-type")[0]).text().strip()
        bullets = [pq(b).text() for b in pq("article ul:first-of-type li")][:3]
        strongs = [pq(s) for s in pq("article strong")]
        offset, _ = next((s for s in enumerate(strongs)
                          if "should say" in s[1].text()), (-1, None))
        if offset == None or offset >= len(strongs)-1:
            return None
        prompt = strongs[offset].text()
        ending = strongs[offset+1].text().split('/n')[0]
        return Cue(title, prompt, bullets, ending)


async def call_for_hrefs(url):
    async with aiohttp.ClientSession() as session, session.get(url=url) as response:
        resp = await response.read()
        pq = PyQuery(resp)
        links = pq('.list-title a[href^="/cue-card-sample/"]')
        hrefs = [pq(link).attr('href') for link in links]
        return hrefs


async def call_for_cues(href):
    async with aiohttp.ClientSession() as session, session.get(url=BASE_URL+href) as response:
        resp = await response.read()
        return Cue.from_markup(resp)


async def get_hrefs(urls):
    hrefs = await asyncio.gather(*[call_for_hrefs(url) for url in urls])
    hrefs = [href for sub in hrefs for href in sub]
    return hrefs


async def get_cues(hrefs):
    cues = await asyncio.gather(*[call_for_cues(href) for href in hrefs])
    cues = [cue for cue in cues if cue != None]
    return cues


def parse_args():
    args = parser.parse_args()
    output_type = args.output.split('.')[-1]
    if output_type not in ['txt', 'db']:
        raise ValueError("Output type has to be either txt or db")
    return args, output_type


def save_to_txt(cues, output):
    with open(output, "w+") as file:
        [file.write(str(cue)+'\n\n') for cue in cues]


def save_to_db(cues, output):
    if os.path.exists(output):
        os.remove(output)
    with sqlite3.connect(output) as c:
        c.execute(
            'CREATE TABLE cards (title text, prompt text, bullets text, ending text)')
        c.executemany('INSERT INTO cards VALUES (?, ?, ?, ?)', [
                      [cue.title, cue.prompt, '\n'.join(cue.bullets), cue.ending] for cue in cues])


def main():
    args, output_type = parse_args()
    urls = [f'{CARDS_URL}?start={start}' for start in range(0, args.limit, 20)]

    hrefs = asyncio.run(get_hrefs(urls))
    cues = asyncio.run(get_cues(hrefs))

    if output_type == 'txt':
        save_to_txt(cues, args.output)
    else:
        save_to_db(cues, args.output)


if __name__ == "__main__":
    main()
