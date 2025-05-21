import requests
from bs4 import BeautifulSoup
import time
import random
import csv

# League URL and base
base_url = "https://www.transfermarkt.co.uk"
league_url = "https://www.transfermarkt.co.uk/premier-league/startseite/wettbewerb/GB1/plus/?saison_id=2016"

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/125.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.google.com/",
}

session = requests.Session()

# Scrape player URLs for a team
def get_player_urls(team_name, team_url):
    print(f"\nRetrying: {team_name}")
    time.sleep(random.uniform(5, 8))

    response = session.get(team_url, headers=headers)
    if response.status_code != 200:
        print(f" - Failed again (HTTP {response.status_code})")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    player_data = []

    table = soup.find("table", class_="items")
    if table:
        for row in table.find_all("tr", class_=["odd", "even"]):
            link_tag = row.find("td", class_="hauptlink").find("a", href=True)
            if link_tag:
                player_name = link_tag.text.strip()
                player_url = base_url + link_tag["href"].split("?")[0]
                player_data.append((team_name, player_name, player_url))

    if not player_data:
        print(f" - Still no players found for {team_name}")
    return player_data

# Main
def main():
    all_players = []
    failed_team_name = 'AFC Bournemouth'
    failed_team_url = 'https://www.transfermarkt.co.uk/afc-bournemouth/startseite/verein/989/saison_id/2016'

    print(f"\nRetrying {failed_team_name}")

    players = get_player_urls(failed_team_name, failed_team_url)
    all_players.extend(players)

    # Append to CSV (or change to 'w' to overwrite)
    with open("premier_league_2016_17_players.csv", "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for row in all_players:
            writer.writerow(row)

    print(f"\n✅ Retried teams complete. {len(all_players)} new players added.")

if __name__ == "__main__":
    main()
