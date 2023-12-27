import csv
from urllib.parse import urlparse
from search_engines import Google

# Get user input for the search query, or use a default query
user_query = input("Enter your search query (press Enter for default): ")
default_query = 'site:pl intitle:"sklep internetowy" OR intitle:"e-sklep" OR intitle:"internetowy sklep" OR inurl:"sklep-online" OR inurl:"sklep" OR inurl:"shop" OR inurl:"produkty" -oferta -tworzenie -stwórz -wskazówek -załóż -założenie -integracje'
search_query = user_query or default_query

# Perform the Google search
engine = Google()
results = engine.search(search_query)
links = results.links()

# Extract unique domains from the links
unique_domains = set()
for link in links:
    domain = urlparse(link).netloc
    if domain not in unique_domains:
        unique_domains.add(domain)

# Specify the file name where you want to save the unique domains in CSV format
csv_file_name = "google_domains.csv"

# Open the CSV file in write mode and write the header and unique domains
with open(csv_file_name, "w", newline="", encoding="utf-8") as csv_file:
    csv_writer = csv.writer(csv_file)

    # Write the header
    csv_writer.writerow(["domain"])

    # Write each unique domain in a new row
    for domain in unique_domains:
        csv_writer.writerow([domain])

print(f"Domains saved to {csv_file_name}")
