import csv

# Input and output filenames
input_file = 'manual_positions.csv'
output_file = 'final_manual_positions.csv'


# Read and filter rows
with open(input_file, mode='r', newline='', encoding='utf-8') as infile:
    reader = csv.DictReader(infile)

    output_fieldnames = [field for field in reader.fieldnames if field != 'URL']

    # Write filtered rows to a new CSV
    with open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=output_fieldnames)
        writer.writeheader()

        for row in reader:
            filtered_row = {key: value for key, value in row.items() if key != 'URL'}
            writer.writerow(filtered_row)

print(f"Filtered data written to {output_file}")
