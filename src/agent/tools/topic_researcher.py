from crewai_tools import TavilySearchTool

class TopicResearcherTool:
    def __init__(self):
        self.name = "topic_researcher"
    
    def search_topic(self, topic: str):
        """Researches a topic on the web.
        
        Args:
            topic: The topic to research.
            
        Returns:
            A summary of search results.
        """
        try:
            tool = TavilySearchTool()
            result = tool.run(query=topic)
            return result
        except Exception as e:
            return f"Error researching topic: {e}"
