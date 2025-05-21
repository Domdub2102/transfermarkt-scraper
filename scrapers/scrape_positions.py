import csv
import requests
from bs4 import BeautifulSoup
import time
import random
import os

INPUT_FILE = 'test.csv'
OUTPUT_FILE = 'players_with_positions.csv'

USER_AGENTS = [
    # Chrome (Windows)
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",

    # Chrome (macOS)
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_4) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",

    # Firefox (Windows)
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",

    # Firefox (macOS)
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_4; rv:125.0) Gecko/20100101 Firefox/125.0",

    # Safari (macOS)
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_4) AppleWebKit/605.1.15 "
    "(KHTML, like Gecko) Version/16.4 Safari/605.1.15",

    # Edge (Windows)
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.2478.80",

    # Chrome (Linux)
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",

    # Brave (Windows)
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Brave/124.1.64.122",

    # Opera (Windows)
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 OPR/98.0.4759.39",

    # Mobile Chrome (Android)
    "Mozilla/5.0 (Linux; Android 13; Pixel 6) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",

    # Mobile Safari (iPhone)
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 "
    "(KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
]


def get_session():
    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://www.google.com",
        "DNT": "1",  # Do Not Track
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }
    s = requests.Session()
    s.headers.update(headers)
    return s

def get_position_from_url(url):
    try:
        session = get_session()
        response = session.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all <li class="data-header__label"> and look for the one that contains "Position:"
        li_tags = soup.find_all('li', class_='data-header__label')
        for li in li_tags:
            if 'Position:' in li.get_text(strip=True):
                span = li.find('span')
                if span:
                    return span.text.strip()
    except Exception as e:
        print(f"Error fetching {url}: {e}")
    return "Unknown"

def scrape_positions():
    file_exists = os.path.isfile(OUTPUT_FILE)

    with open(INPUT_FILE, 'r', newline='', encoding='utf-8') as infile, \
         open(OUTPUT_FILE, 'a', newline='', encoding='utf-8') as outfile:

        reader = csv.DictReader(infile)
        fieldnames = ['Team', 'Player', 'Position']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        for row in reader:
            url = row['URL']
            print(f"Fetching position for {row['Player']}...")
            position = get_position_from_url(url)
            writer.writerow({
                'Team': row['Team'],
                'Player': row['Player'],
                'Position': position
            })
            #time.sleep(random.uniform(1,2))
    

    print(f"\n✅ Done. Data written to {OUTPUT_FILE}")

if __name__ == "__main__":
    scrape_positions()
