"""GitHub Repository Analyst Agent - Specialized agent for analyzing GitHub repositories."""

from google.adk import Agent
from google.adk.models import Gemini
from ..tools.github_reader import GitHubReader
from ..prompts.github_repo_agent_instructions import GITHUB_REPO_AGENT_INSTRUCTION


def create_github_repo_agent() -> Agent:
    """Creates and configures the GitHub Repository Analyst agent.
    
    This agent specializes in:
    - Cloning GitHub repositories
    - Analyzing repository structure
    - Extracting key files and information
    - Providing comprehensive repository summaries
    
    Returns:
        Agent: Configured GitHub repo agent
    """
    model = Gemini(model="gemini-2.5-flash")
    
    # Initialize the GitHub reader tool
    github_reader = GitHubReader()
    
    # Create the agent with the GitHub reader tool
    agent = Agent(
        model=model,
        name="github_repo_agent",
        instruction=GITHUB_REPO_AGENT_INSTRUCTION,
        tools=[github_reader.read_repo]
    )
    
    return agent
