import os
import sys
from dotenv import load_dotenv
from google.adk import Agent, Runner
from google.adk.models import Gemini
from google.adk.sessions import InMemorySessionService

# Import sub-agents
from .agents import (
    create_github_repo_agent,
    create_blog_reader_agent,
    create_topic_researcher_agent
)

# Import prompts
from .prompts.instructions import MAIN_AGENT_INSTRUCTION

# Load environment variables
load_dotenv()

def create_agent():
    """Creates and configures the Knowledge Flow Orchestrator Agent."""
    
    model = Gemini(model="gemini-2.5-flash")
    
    # Initialize sub-agents
    github_repo_agent = create_github_repo_agent()
    blog_reader_agent = create_blog_reader_agent()
    topic_researcher_agent = create_topic_researcher_agent()
    
    # Create orchestrator agent with sub-agents
    # ADK's hierarchical delegation: sub-agents are passed via sub_agents parameter
    # This gives the parent agent an implicit transfer_to_agent tool for delegation
    agent = Agent(
        model=model,
        name="knowledge_flow_orchestrator",
        instruction=MAIN_AGENT_INSTRUCTION,
        sub_agents=[
            github_repo_agent,
            blog_reader_agent,
            topic_researcher_agent
        ]
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
