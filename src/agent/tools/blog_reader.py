import requests
from bs4 import BeautifulSoup

class BlogReader:
    def __init__(self):
        self.name = "blog_reader"
    
    def read_blog(self, blog_url: str):
        """Reads and summarizes a blog post.
        
        Args:
            blog_url: The URL of the blog post.
            
        Returns:
            A summary of the blog content.
        """
        try:
            response = requests.get(blog_url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Basic extraction: Title and paragraphs
            title = soup.title.string if soup.title else "No Title"
            paragraphs = soup.find_all('p')
            text_content = "\n".join([p.get_text() for p in paragraphs])
            
            # Truncate for MVP
            summary = text_content[:1000] + "..." if len(text_content) > 1000 else text_content
            
            return f"Read blog: {title}\n\nContent Summary:\n{summary}"
            
        except Exception as e:
            return f"Error reading blog: {e}"
