from crewai_tools import ScrapeWebsiteTool

class WebScraperTool:
    def __init__(self):
        self.name = "web_scraper"
    
    def scrape_website(self, url: str) -> str:
        """Scrape and extract content from a website URL.

        Args:
            url: The URL of the website to scrape

        Returns:
            The scraped content from the website
        """
        try:
            tool = ScrapeWebsiteTool(website_url=url)
            result = tool.run()
            return result   
        except Exception as e:
            return f"Error scraping website: {e}"
