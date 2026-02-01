import requests

class MarktplaatsVehicleScraper:
    """
    A production-style scraper for Marktplaats.nl (Cars/Vehicles category).
    Uses internal API endpoints for high performance and data accuracy.
    """

    def __init__(self):
        # Target API endpoint identified from network inspection
        self.api_url = "https://www.marktplaats.nl/lrp/api/search?attributesById[]=10882&l1CategoryId=91&limit=30&offset=0&viewOptions=list-view"
        
        # Standard headers to mimic a browser request
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json",
        }

    def fetch_listings(self):
        """Fetches raw JSON data from the internal backend API."""
        try:
            response = requests.get(self.api_url, headers=self.headers, timeout=10)
            response.raise_for_status()  # Ensure we handle HTTP errors
            return response.json().get('listings', [])
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return []

    def format_price(self, price_info):
        """
        Parses the nested priceInfo object.
        Converts priceCents to a human-readable Euro format.
        """
        cents = price_info.get('priceCents')
        if cents:
            # Convert cents to Euro and format with thousand separators
            return f"€{cents / 100:,.2f}"
        return "Bieden / Negotiable"

    def extract_attributes(self, attribute_list):
        """
        Maps the list of attributes to a dictionary for O(1) lookup.
        Target keys: 'fuel', 'transmission' as per Data Contract.
        """
        return {attr.get('key'): attr.get('value') for attr in attribute_list}

    def run(self):
        """Main execution logic to process and display vehicle listings."""
        listings = self.fetch_listings()
        
        if not listings:
            print("No listings found or API access blocked.")
            return

        print(f"{'TITLE':<50} | {'PRICE':<12} | {'FUEL':<10} | {'GEARBOX'}")
        print("-" * 90)

        for item in listings:
            # 1. Extract Identity & Title
            title = item.get('title', 'Unknown Title')
            
            # 2. Extract Price from the nested priceInfo
            price = self.format_price(item.get('priceInfo', {}))
            
            # 3. Extract Technical Specs from attributes
            attrs = self.extract_attributes(item.get('attributes', []))
            fuel = attrs.get('fuel', 'N/A')
            transmission = attrs.get('transmission', 'N/A')

            # 4. Conform to daily run requirements (Stable IDs could be added here)
            print(f"{title[:48]:<50} | {price:<12} | {fuel:<10} | {transmission}")

if __name__ == "__main__":
    # Initialize and execute the scraper
    scraper = MarktplaatsVehicleScraper()
    scraper.run()