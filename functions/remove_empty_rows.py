import csv

# Input and output filenames
input_file = 'injuries_and_suspensions_final.csv'
output_file = 'injuries_and_suspensions_long.csv'

# Helper function to extract the number from "days" field
def parse_days(days_str):
    try:
        return int(days_str.strip().split()[0])
    except (ValueError, AttributeError, IndexError):
        return 0

# Read and filter rows
with open(input_file, mode='r', newline='', encoding='utf-8') as infile:
    reader = csv.DictReader(infile)
    filtered_rows = [row for row in reader if parse_days(row['days']) > 100]

# Write filtered rows to a new CSV
with open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
    writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
    writer.writeheader()
    writer.writerows(filtered_rows)

print(f"Filtered data written to {output_file}")
