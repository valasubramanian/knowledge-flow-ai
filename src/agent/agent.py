import os
import sys
from dotenv import load_dotenv
from google.adk import Agent, Runner
from google.adk.models import Gemini
from google.adk.sessions import InMemorySessionService

# Import tools
from .tools.github_reader import GitHubReader
from .tools.blog_reader import BlogReader
from .tools.topic_researcher import TopicResearcher

# Import prompts
from .prompts.instructions import MAIN_AGENT_INSTRUCTION

# Load environment variables
load_dotenv()

def create_agent():
    """Creates and configures the Knowledge Flow Main Agent."""
    
    model = Gemini(model="gemini-2.5-flash")
    
    # Initialize tools
    github_reader = GitHubReader()
    blog_reader = BlogReader()
    topic_researcher = TopicResearcher()
    
    # Define tools list
    tools = [
        github_reader.read_repo,
        blog_reader.read_blog,
        topic_researcher.research_topic
    ]
    
    agent = Agent(
        model=model,
        name="knowledge_flow_orchestrator",
        instruction=MAIN_AGENT_INSTRUCTION,
        tools=tools
    )
    return agent

# Create the agent instance for adk web to discover
root_agent = create_agent()

def main():
    """Main entry point for the agent."""
    if not os.getenv("GOOGLE_API_KEY"):
        print("Error: GOOGLE_API_KEY not found in environment variables.")
        print("Please create a .env file with your GOOGLE_API_KEY.")
        return

    # Use the global agent instance
    session_service = InMemorySessionService()
    runner = Runner(
        agent=root_agent, 
        session_service=session_service,
        app_name="knowledge_flow_app"
    )
    
    # Use run_live for web-based debugging if supported/requested, otherwise default to run loop
    # For now, we keep the CLI loop but expose the runner.
    # If the user wants to use 'adk web', they typically run `adk web path/to/agent`
    # But to "enable" it, we might need to ensure the agent is importable.
    
    print("Knowledge Flow Agent initialized. Type 'exit' to quit.")
    
    while True:
        try:
            user_input = input("You: ")
            if user_input.lower() in ["exit", "quit"]:
                break
            
            # Basic interaction loop
            response = runner.run(user_input)
            print(f"Agent: {response}")
            
        except EOFError:
            break
        except Exception as e:
            print(f"Error executing agent: {e}")

if __name__ == "__main__":
    main()
