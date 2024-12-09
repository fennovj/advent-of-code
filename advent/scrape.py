import os
import requests

def scrape(year: int, day: int, extension: str = 'txt'):
    if os.path.exists(f"data/advent{day}.{extension}"):
        return # Prevent spamming
    with open('../session.txt', 'r') as f:
        session = f.read()
    if session.startswith('session='):
        session = session[8:]
    response = requests.get(
        f"https://adventofcode.com/{year}/day/{day}/input",
        cookies={'session': session},
        headers = {'User-Agent': 'AoC Downloader'}
    )
    response.raise_for_status()
    with open(f"data/advent{day}.{extension}", 'w') as f:
        f.write(response.text)