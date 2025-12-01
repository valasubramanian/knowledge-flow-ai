"""LinkedIn Sharer Agent - Specialized agent for sharing articles on LinkedIn."""

from google.adk import Agent
from google.adk.models import Gemini
from ..tools.linkedin_sharer import LinkedInSharerTool
from ..prompts.linkedin_sharer_agent_instructions import LINKEDIN_SHARER_AGENT_INSTRUCTION


def create_linkedin_sharer_agent() -> Agent:
    """Creates and configures the LinkedIn Sharer agent.
    
    This agent specializes in:
    - Summarizing articles for LinkedIn
    - Interacting with the user to refine the post
    - Posting to LinkedIn via API
    
    This agent is designed to be a sub-agent of:
    - article_deployer_agent
    
    Returns:
        Agent: Configured LinkedIn sharer agent
    """
    model = Gemini(model="gemini-2.0-flash")
    
    # Initialize the LinkedIn sharer tool
    sharer = LinkedInSharerTool()
    
    # Create the agent
    agent = Agent(
        model=model,
        name="linkedin_sharer_agent",
        instruction=LINKEDIN_SHARER_AGENT_INSTRUCTION,
        tools=[
            sharer.post_article_summary
        ]
    )
    
    return agent
