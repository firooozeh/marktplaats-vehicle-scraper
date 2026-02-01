import requests
import csv

class MarktplaatsVehicleScraper:
    """
    A professional scraper for Marktplaats.nl vehicle listings.
    Fetches data from internal API, supports pagination, and exports to CSV.
    """

    def __init__(self):
        # Base API URL without the offset parameter
        self.base_url = "https://www.marktplaats.nl/lrp/api/search?attributesById[]=10882&l1CategoryId=91&limit=30&viewOptions=list-view"
        
        # Standard headers to mimic a real browser
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        
        # List to store collected dictionaries for all pages
        self.all_listings = []

    def format_price(self, price_info):
        """Converts raw price cents from API into a formatted Euro string."""
        cents = price_info.get('priceCents')
        if cents:
            return f"€{cents / 100:,.2f}"
        return "Bieden" # Handling 'Bidding' cases

    def extract_attributes(self, attribute_list):
        """Flattens the nested attributes list into a searchable dictionary."""
        return {attr.get('key'): attr.get('value') for attr in attribute_list}

    def save_to_csv(self, filename="marktplaats_cars.csv"):
        """Exports the gathered data into a CSV file for Excel analysis."""
        headers = ["Title", "Price", "Fuel", "Transmission"]
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=headers)
                writer.writeheader()
                writer.writerows(self.all_listings)
            print(f"\n[SUCCESS] Extracted {len(self.all_listings)} listings to {filename}")
        except IOError as e:
            print(f"[ERROR] Could not save to CSV: {e}")

    def run(self, total_pages=5):
        """Main execution logic to loop through pages and collect data."""
        print(f"[START] Beginning extraction for {total_pages} pages...")

        for page in range(total_pages):
            # Calculate offset for pagination (30 items per page)
            offset = page * 30
            request_url = f"{self.base_url}&offset={offset}"
            
            try:
                response = requests.get(request_url, headers=self.headers, timeout=10)
                response.raise_for_status() # Check for HTTP errors
                data = response.json()
                listings = data.get('listings', [])

                if not listings:
                    print(f"No more data found at page {page}. Stopping.")
                    break

                for item in listings:
                    attrs = self.extract_attributes(item.get('attributes', []))
                    
                    # Structuring the final object
                    car_record = {
                        "Title": item.get('title', 'N/A'),
                        "Price": self.format_price(item.get('priceInfo', {})),
                        "Fuel": attrs.get('fuel', 'N/A'),
                        "Transmission": attrs.get('transmission', 'N/A')
                    }
                    self.all_listings.append(car_record)

                print(f"Successfully processed Page {page + 1}")

            except Exception as e:
                print(f"[ERROR] Failed to fetch Page {page + 1}: {e}")
                break

        # Final step: Save all results to disk
        self.save_to_csv()

if __name__ == "__main__":
    # Instantiate and run the scraper
    scraper = MarktplaatsVehicleScraper()
    scraper.run(total_pages=5) # You can adjust the number of pages here