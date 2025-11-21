"""Topic Research Specialist Agent - Specialized agent for researching technical topics."""

from google.adk import Agent
from google.adk.models import Gemini
from google.adk.tools import google_search
from ..prompts.topic_researcher_agent_instructions import TOPIC_RESEARCHER_AGENT_INSTRUCTION


def create_topic_researcher_agent() -> Agent:
    """Creates and configures the Topic Research Specialist agent.
    
    This agent specializes in:
    - Searching the web for technical topics
    - Aggregating and synthesizing search results
    - Providing comprehensive topic overviews
    - Finding relevant resources and documentation
    
    Returns:
        Agent: Configured topic researcher agent
    """
    model = Gemini(model="gemini-2.5-flash")
    
    # Create the agent with the Google search tool
    agent = Agent(
        model=model,
        name="topic_researcher_agent",
        instruction=TOPIC_RESEARCHER_AGENT_INSTRUCTION,
        tools=[google_search]
    )
    
    return agent
