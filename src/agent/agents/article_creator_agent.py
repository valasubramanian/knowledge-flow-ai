"""Article Creator Agent - Specialized agent for creating technical articles with human-in-the-loop workflow."""

from google.adk import Agent
from google.adk.models import Gemini
from ..tools.article_creator import ArticleCreatorTool
from ..prompts.article_creator_agent_instructions import ARTICLE_CREATOR_AGENT_INSTRUCTION


def create_article_creator_agent() -> Agent:
    """Creates and configures the Article Creator agent.
    
    This agent specializes in:
    - Creating article structures for user approval
    - Generating article content based on source information
    - Iterative refinement with human-in-the-loop
    - Writing in the user's voice and style
    - Preparing articles for deployment
    
    This agent is designed to be a sub-agent of:
    - github_repo_agent
    - blog_reader_agent
    - topic_researcher_agent
    
    And has its own sub-agent:
    - article_deployer_agent
    
    Returns:
        Agent: Configured article creator agent with article creation tools
    """
    model = Gemini(model="gemini-2.0-flash")
    
    # Initialize the article creator tool
    article_creator = ArticleCreatorTool()
    
    # Import article deployer agent here to avoid circular imports
    from .article_deployer_agent import create_article_deployer_agent
    article_deployer_agent = create_article_deployer_agent()
    
    # Create the agent with article creation tools and article deployer as sub-agent
    agent = Agent(
        model=model,
        name="article_creator_agent",
        instruction=ARTICLE_CREATOR_AGENT_INSTRUCTION,
        tools=[
            article_creator.create_article_structure,
            article_creator.generate_article_content,
            article_creator.refine_article_section,
            article_creator.list_articles,
        ],
        sub_agents=[
            article_deployer_agent
        ]
    )
    
    return agent
