import csv

# Input and output filenames
input_file = '/Users/marinaag/Desktop/Dom Coding/transfermarkt-scraper/csv_final/players_with_positions.csv'
output_file = '/Users/marinaag/Desktop/Dom Coding/transfermarkt-scraper/csv_final/final_players.csv'


def update_position(string):
    if 'Back' in string:
        return 'Defender'
    elif 'Midfield' in string or 'Winger' in string:
        return 'Midfielder'
    elif 'Forward' in string or 'Striker' in string:
        return 'Forward'
    else: return string

# Read and filter rows
with open(input_file, mode='r', newline='', encoding='utf-8') as infile:
    reader = csv.DictReader(infile)

    # Write filtered rows to a new CSV
    with open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
        writer.writeheader()
        
        for row in reader:
            position = update_position(row['Position'])
            writer.writerow({
                'Team': row['Team'],
                'Player': row['Player'],
                'Position': position
            })

print(f"Filtered data written to {output_file}")