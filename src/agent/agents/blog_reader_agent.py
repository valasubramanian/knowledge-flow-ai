"""Blog Content Analyst Agent - Specialized agent for scraping and analyzing web content."""

from google.adk import Agent
from google.adk.models import Gemini
from ..tools.web_scraper import WebScraper
from ..prompts.blog_reader_agent_instructions import BLOG_READER_AGENT_INSTRUCTION


def create_blog_reader_agent() -> Agent:
    """Creates and configures the Blog Content Analyst agent.
    
    This agent specializes in:
    - Scraping blog posts and web pages
    - Extracting main content from HTML
    - Summarizing technical articles
    - Identifying key insights and takeaways
    
    Returns:
        Agent: Configured blog reader agent
    """
    model = Gemini(model="gemini-2.5-flash")
    
    # Initialize the web scraper tool
    web_scraper = WebScraper()
    
    # Create the agent with the web scraper tool
    agent = Agent(
        model=model,
        name="blog_reader_agent",
        instruction=BLOG_READER_AGENT_INSTRUCTION,
        tools=[web_scraper.scrape_website]
    )
    
    return agent
