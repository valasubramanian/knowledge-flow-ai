from crewai_tools import ScrapeWebsiteTool

class WebScraper:
    def __init__(self):
        self.name = "web_scraper"
        self._tool = ScrapeWebsiteTool()
    
    def scrape_website(self, url: str) -> str:
        """Scrape and extract content from a website URL.

        Args:
            url: The URL of the website to scrape

        Returns:
            The scraped content from the website
        """
        try:
            result = self._tool.run(url)
            return result
        except Exception as e:
            return f"Error scraping website: {e}"
