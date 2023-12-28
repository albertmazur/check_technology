import csv
from urllib.parse import urlparse
from search_engines import Google, Bing, Yahoo

# Get user input for the search query, or use a default query
user_query = input("Enter your search query (press Enter for default): ")
default_query = 'site:pl intitle:"sklep internetowy" OR intitle:"e-sklep" OR intitle:"internetowy sklep" OR inurl:"sklep-online" OR inurl:"sklep" OR inurl:"shop" OR inurl:"produkty" -oferta -tworzenie -stwórz -wskazówek -załóż -założenie -integracje'
search_query = user_query or default_query

# Perform the Google search
google_engine = Google()
google_results = google_engine.search(search_query)
google_links = google_results.links()

# Perform the Bing search
bing_engine = Bing()
bing_results = bing_engine.search(search_query)
bing_links = bing_results.links()

# Perform the Yahoo search
yahoo_engine = Yahoo()
yahoo_results = yahoo_engine.search(search_query)
yahoo_links = yahoo_results.links()

# Combine links from all search engines
all_links = google_links + bing_links + yahoo_links

# Extract unique domains from the links
unique_domains = set()
for link in all_links:
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
