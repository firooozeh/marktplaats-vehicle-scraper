# Marktplaats Vehicle Scraper (API-Based)

A professional, production-style Python scraper designed to extract vehicle listings from Marktplaats.nl using internal API endpoints.

## 🚀 Key Features
- **API-First Strategy**: Bypasses slow HTML scraping by directly interfacing with Marktplaats' internal JSON backend for maximum speed and data integrity.
- **Production-Ready Code**: Implemented using a clean, class-based architecture to ensure maintainability and easy integration into existing repositories.
- **Data Accuracy**: Precisely extracts nested data including technical specifications (Fuel type, Transmission) and converts raw price cents into formatted Euros.
- **Standard Repo Structure**: Includes dependency management via `requirements.txt` and professional documentation.

## 🛠️ Requirements
- Python 3.11+
- `requests` library

## ⚙️ Installation & Usage
1. Clone this repository to your local machine.
2. Install the necessary dependencies:
   ```bash
   pip install -r requirements.txt

3. Run the main scraper script:
   ```bash
   python main.py


## 📊 Sample Output
The scraper extracts and formats data directly from the Marktplaats API. Here is an example of the structured output:

| TITLE | PRICE | FUEL | GEARBOX |
| :--- | :--- | :--- | :--- |
| Audi A4 B8 88kw 1.8 tfsi 2010 wit | €4,000.00 | Benzine | Handgeschakeld |
| Suzuki Wagon R+ 1.3 2003 5D Zwart | €1,450.00 | Benzine | Handgeschakeld |
| Lexus RX 450h AWD President Line | €49,950.00 | Hybride | Automaat |
| BMW X1 xDrive25e M-sport | €44,950.00 | Hybride | Automaat |
| Dodge Ram (Bidding) | Bieden | LPG | Automaat |

> **Note**: Pricing is automatically converted from cents to formatted Euros. Technical attributes are mapped from the API's nested JSON structure.