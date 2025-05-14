import csv
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import random
import os

# --- Settings ---
INPUT_CSV = "premier_league_2016_17_players.csv"
OUTPUT_CSV = "injuries_and_suspensions_2016_17.csv"
START_DATE = datetime(2016, 8, 13)
END_DATE = datetime(2017, 5, 21)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/125.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}

session = requests.Session()

def parse_date(date_str):
    try:
        return datetime.strptime(date_str.strip(), "%b %d, %Y")
    except ValueError:
        return None

def extract_events(base_url, event_type):
    page = 1
    all_events = []

    while True:
        paginated_url = f"{base_url}/page/{page}"
        print(f"url: {paginated_url}")
        time.sleep(random.uniform(2, 5))

        response = session.get(paginated_url, headers=HEADERS)
        if response.status_code != 200:
            print(f" - Failed to fetch {event_type} page {page}: {paginated_url}")
            break

        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find("table", class_="items")
        if not table:
            break

        rows = table.find_all("tr", class_=["even", "odd"])
        if not rows:
            break

        for row in rows:
            cells = row.find_all("td")
            try:
                if event_type == "injury":
                    reason = cells[1].text.strip()
                    start_date = parse_date(cells[2].text.strip())
                    end_date = parse_date(cells[3].text.strip())
                    days = cells[4].text.strip()

                elif event_type == "suspension":
                    
                    reason = cells[1].text.strip()
                    start_date = parse_date(cells[3].text.strip())
                    end_date = parse_date(cells[4].text.strip())
                    days = cells[5].text.strip()
                else:
                    continue

                if start_date and end_date and start_date <= END_DATE and end_date >= START_DATE:
                    all_events.append({
                        "event_type": event_type,
                        "reason": reason,
                        "start_date": start_date.strftime("%Y-%m-%d"),
                        "end_date": end_date.strftime("%Y-%m-%d"),
                        "days": days,
                    })
            except Exception as e:
                print(f" - Skipping row due to error: {e}")
                continue

        # Stop if no "next page" link
        pagination_next = soup.find("li", class_="tm-pagination__list-item--icon-next-page")
        if pagination_next is None:
            break

        page += 1

    return all_events

def main():
    headers = [
        "team", "player", "event_type", "reason",
        "start_date", "end_date", "days", "url"
    ]

    # Prepare CSV writer
    file_exists = os.path.exists(OUTPUT_CSV)
    with open(OUTPUT_CSV, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        if not file_exists or os.stat(OUTPUT_CSV).st_size == 0:
            writer.writeheader()

        # Read input players
        with open(INPUT_CSV, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip header
            players = list(reader)

        print(f"Processing {len(players)} players...")

        for team, player, url in players:
            print(f"\n{player} ({team})")

            injury_url = url.replace("profil", "verletzungen")
            suspension_url = url.replace("profil", "ausfaelle")

            injuries = extract_events(injury_url, "injury")
            suspensions = extract_events(suspension_url, "suspension")

            combined_events = injuries + suspensions

            if not combined_events:
                # Write empty placeholder row
                writer.writerow({
                    "team": team,
                    "player": player,
                    "event_type": "none",
                    "reason": "",
                    "start_date": "",
                    "end_date": "",
                    "days": "",
                    "url": url
                })
                f.flush()
                continue

            for event in combined_events:
                writer.writerow({
                    "team": team,
                    "player": player,
                    "event_type": event["event_type"],
                    "reason": event["reason"],
                    "start_date": event["start_date"],
                    "end_date": event["end_date"],
                    "days": event["days"],
                    "url": url
                })
            f.flush()

    print(f"\n✅ Done! Processed {len(players)} players. Data appended to: {OUTPUT_CSV}")

if __name__ == "__main__":
    main()
