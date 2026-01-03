import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import logging

# Configure logging for tracking the automation process
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class MarketScraper:
    def __init__(self, url):
        self.url = url
        self.data = []

    def fetch_data(self):
        """Fetches raw HTML from the target URL."""
        try:
            logging.info(f"Connecting to {self.url}...")
            response = requests.get(self.url, headers={"User-Agent": "Mozilla/5.0"})
            if response.status_code == 200:
                logging.info("Connection successful.")
                return response.content
            else:
                logging.error(f"Failed to connect. Status Code: {response.status_code}")
                return None
        except Exception as e:
            logging.error(f"Error occurred: {e}")
            return None

    def parse_html(self, html_content):
        """Parses HTML to extract headlines and dates."""
        if not html_content:
            return
        
        soup = BeautifulSoup(html_content, 'html.parser')
        articles = soup.find_all('div', class_='news-item') # Placeholder class

        for article in articles:
            title = article.find('h2').text.strip()
            date = datetime.datetime.now().strftime("%Y-%m-%d")
            self.data.append({'Date': date, 'Title': title, 'Source': 'FinancialWeb'})
        
        logging.info(f"Extracted {len(self.data)} articles.")

    def save_to_excel(self, filename="market_data.xlsx"):
        """Saves the extracted data to an Excel file."""
        if self.data:
            df = pd.DataFrame(self.data)
            df.to_excel(filename, index=False)
            logging.info(f"Data saved to {filename}")
        else:
            logging.warning("No data to save.")

if __name__ == "__main__":
    # Example usage
    TARGET_URL = "https://example-financial-news-site.com" 
    bot = MarketScraper(TARGET_URL)
    html = bot.fetch_data()
    bot.parse_html(html)
    bot.save_to_excel()
