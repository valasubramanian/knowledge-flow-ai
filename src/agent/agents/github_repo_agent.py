"""GitHub Repository Analyst Agent - Specialized agent for analyzing GitHub repositories."""

from google.adk import Agent
from google.adk.models import Gemini
from ..tools.github_reader import GitHubReaderTool
from ..prompts.github_repo_agent_instructions import GITHUB_REPO_AGENT_INSTRUCTION
from ..utils.repository_analyzer import RepositoryAnalyzer


def create_github_repo_agent() -> Agent:
    """Creates and configures the GitHub Repository Analyst agent.
    
    This agent specializes in:
    - Cloning GitHub repositories
    - Analyzing repository structure
    - Detecting components and functionalities
    - Extracting code snippets
    - Providing comprehensive repository analysis with human-in-the-loop workflow
    
    Returns:
        Agent: Configured GitHub repo agent with analysis tools
    """
    model = Gemini(model="gemini-2.0-flash")
    
    # Initialize the GitHub reader tool
    github_reader = GitHubReaderTool()
    
    # Initialize the repository analyzer with temp_dir
    analyzer = RepositoryAnalyzer()
    
    # Create the agent with multiple tools
    agent = Agent(
        model=model,
        name="github_repo_agent",
        instruction=GITHUB_REPO_AGENT_INSTRUCTION,
        tools=[
            github_reader.clone_repo,
            github_reader.cleanup_repo,
            analyzer.analyze_structure,
            analyzer.detect_components,
            analyzer.read_file,
            analyzer.extract_code_snippets,
        ]
    )
    
    return agent

