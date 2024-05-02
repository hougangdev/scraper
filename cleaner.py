import csv

def clean_price(price):
    cleaned_price = price.replace("$", "").replace(",", "")
    return float(cleaned_price)

def read_and_clean_data(input_file, output_file):
    with open(input_file, 'r', newline='') as infile, open(output_file, 'w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        # read each row in the input csv, clean it, and write to output csv
        for row in reader:
            if row: # if row is not empty
                cleaned_price = clean_price(row[0])
                writer.writerow([cleaned_price])
                
# specify input and output file name
input_csv = 'volume.csv'
output_csv = 'cleaned_volume.csv'

read_and_clean_data(input_csv, output_csv)
