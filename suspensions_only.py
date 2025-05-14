import csv
import requests
from bs4 import BeautifulSoup
from datetime import datetime

INPUT_CSV = "test.csv"
OUTPUT_CSV = "filtered_suspensions_2016_17.csv"

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

def extract_premier_league_suspensions(url):
    page = 1
    all_events = []

    while True:
        paginated_url = f"{url}/page/{page}"
        print(f"Fetching: {paginated_url}")
        #time.sleep(random.uniform(0, 1))

        response = session.get(paginated_url, headers=HEADERS)
        if response.status_code != 200:
            print(f" - Failed to fetch: {paginated_url}")
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
            if len(cells) < 6:
                continue

            # Filter only Premier League
            comp_img = cells[2].find("img")
            if not comp_img or comp_img.get("title") == "Premier League":
                continue

            reason = cells[1].text.strip()
            start_date = parse_date(cells[3].text.strip())
            end_date = parse_date(cells[4].text.strip())
            days = cells[5].text.strip()

            if start_date and end_date and start_date <= END_DATE and end_date >= START_DATE:
                all_events.append({
                    "competition": comp_img.get("title"),
                    "reason": reason,
                    "start_date": start_date.strftime("%Y-%m-%d"),
                    "end_date": end_date.strftime("%Y-%m-%d"),
                    "days": days
                })

        # Pagination end check
        next_btn = soup.find("li", class_="tm-pagination__list-item--icon-next-page")
        if next_btn is None:
            break
        page += 1

    return all_events

def main():
    results = []
    
    with open(INPUT_CSV, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        players = {(row["Team"], row["Player"], row["URL"]) for row in reader}

    for team, player, profile_url in players:
        print(f"Processing {player} ({team})")

        suspension_url = profile_url.replace("profil", "ausfaelle")
        suspensions = extract_premier_league_suspensions(suspension_url)

        if not suspensions:
            print(f" - No valid suspensions for Premier League")
            continue

        for event in suspensions:
            results.append({
                "team": team,
                "player": player,
                "event_type": "suspension",
                "competition": event["competition"],
                "reason": event["reason"],
                "start_date": event["start_date"],
                "end_date": event["end_date"],
                "days": event["days"],
                "url": profile_url
            })

    # Save to CSV
    with open(OUTPUT_CSV, "w", newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=[
            "team", "player", "event_type", "competition", "reason",
            "start_date", "end_date", "days", "url"
        ])
        writer.writeheader()
        writer.writerows(results)

    print(f"\n✅ Done! Saved {len(results)} filtered Premier League suspensions to {OUTPUT_CSV}")

if __name__ == "__main__":
    main()
