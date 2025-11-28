"""Article Deployer Agent - Specialized agent for deploying articles to GitHub Pages."""

from google.adk import Agent
from google.adk.models import Gemini
from ..tools.github_pages_deployer import GitHubPagesDeployerTool
from ..prompts.article_deployer_agent_instructions import ARTICLE_DEPLOYER_AGENT_INSTRUCTION


def create_article_deployer_agent() -> Agent:
    """Creates and configures the Article Deployer agent.
    
    This agent specializes in:
    - Deploying articles to GitHub Pages
    - Managing Jekyll-compatible post creation
    - Handling git operations (clone, commit, push)
    - Validating deployments
    - Providing GitHub Pages URLs
    
    This agent is designed to be a sub-agent of:
    - article_creator_agent
    
    Returns:
        Agent: Configured article deployer agent with GitHub Pages deployment tools
    """
    model = Gemini(model="gemini-2.0-flash")
    
    # Initialize the GitHub Pages deployer tool
    deployer = GitHubPagesDeployerTool()
    
    # Create the agent with deployment tools
    agent = Agent(
        model=model,
        name="article_deployer_agent",
        instruction=ARTICLE_DEPLOYER_AGENT_INSTRUCTION,
        tools=[
            deployer.deploy_article,
            deployer.validate_deployment,
        ]
    )
    
    return agent
