from googlesearch import search

class TopicResearcher:
    def __init__(self):
        self.name = "topic_researcher"
    
    def research_topic(self, topic: str):
        """Researches a topic on the web.
        
        Args:
            topic: The topic to research.
            
        Returns:
            A summary of search results.
        """
        try:
            results = []
            # Perform a simple Google search
            for url in search(topic, num_results=5, advanced=True):
                results.append(f"- {url.title}: {url.url}\n  {url.description}")
            
            return f"Research results for '{topic}':\n\n" + "\n".join(results)
            
        except Exception as e:
            return f"Error researching topic: {e}"
