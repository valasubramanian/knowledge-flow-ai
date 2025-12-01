# Knowledge Flow Agent

The **Knowledge Flow Agent** is an AI-powered developer advocate assistant designed to help you share your technical learnings with the community. It automates the process of researching topics, analyzing code repositories, and summarizing blog posts to generate content for platforms like GitHub Pages and LinkedIn.

Built with [Google's Agent Development Kit (ADK)](https://github.com/google/adk) and Python.

## Features

- **Multi-Agent Architecture**: Hierarchical system with specialized sub-agents
- **Root Orchestrator**: Intelligently routes user requests to appropriate sub-agents
- **GitHub Repository Agent**: Clones and analyzes GitHub repositories with human-in-the-loop for analysis scope
- **Blog Reader Agent**: Scrapes and summarizes web content with human-in-the-loop confirmation
- **Topic Researcher Agent**: Performs web searches and synthesizes information with human-in-the-loop scope confirmation
- **Article Creator Agent**: Creates well-structured technical articles from source information with iterative refinement
- Article Deployer Agent: Deploys articles to GitHub Pages with Jekyll-compatible formatting
- LinkedIn Sharer Agent: Posts summaries of deployed articles to LinkedIn with Human-in-the-Loop refinement
- Human-in-the-Loop Workflow: Interactive refinement at every stage from research to publication

## Prerequisites

- Python 3.10+
- [uv](https://github.com/astral-sh/uv) (Python package manager)
- Google Cloud Project with Vertex AI API enabled (or Google AI Studio API Key)

## Installation

1.  **Clone the repository:**

    ```bash
    git clone <repository-url>
    cd knowledge-flow-ai
    ```

2.  **Set up the environment:**

    ```bash
    uv sync
    ```

3.  **Configure Environment Variables:**
    Create a `.env` file in the root directory:

    ```bash
    cp .env.example .env
    ```

    Edit `.env` and add your API keys:

    ```
    GOOGLE_API_KEY=your_google_api_key_here
    GITHUB_TOKEN=your_github_personal_access_token_here
    LINKEDIN_ACCESS_TOKEN=your_linkedin_access_token_here
    ```

    **Note**:

    - `GITHUB_TOKEN` is required only if you want to deploy articles to GitHub Pages. Get a Personal Access Token from GitHub Settings → Developer settings → Personal access tokens with `repo` permissions.
    - `LINKEDIN_ACCESS_TOKEN` is required for the LinkedIn Sharer Agent.

## Usage

### CLI Mode

Run the agent directly in your terminal:

```bash
uv run src/agent/agent.py
```

### Web Debugger (ADK Web)

Debug and interact with the agent using the ADK Web UI:

```bash
adk web src/agent/agent.py
```

Then open your browser at `http://localhost:8000` (or the port displayed in the output).

## Project Structure

```
knowledge-flow-ai/
├── src/
│   ├── agent/
│   │   ├── agents/              # Sub-agent modules
│   │   │   ├── github_repo_agent.py
│   │   │   ├── blog_reader_agent.py
│   │   │   ├── topic_researcher_agent.py
│   │   │   ├── article_creator_agent.py      # NEW: Article creation
│   │   │   ├── article_deployer_agent.py     # NEW: GitHub Pages deployment
│   │   │   └── linkedin_sharer_agent.py      # NEW: LinkedIn sharing
│   │   ├── tools/               # Tool implementations
│   │   │   ├── github_reader.py
│   │   │   ├── web_scraper.py
│   │   │   ├── topic_researcher.py
│   │   │   ├── article_creator.py            # NEW: Article creation tool
│   │   │   ├── github_pages_deployer.py      # NEW: GitHub Pages tool
│   │   │   └── linkedin_sharer.py            # NEW: LinkedIn tool
│   │   ├── prompts/             # System prompts
│   │   │   ├── instructions.py
│   │   │   ├── github_repo_agent_instructions.py
│   │   │   ├── blog_reader_agent_instructions.py
│   │   │   ├── topic_researcher_agent_instructions.py
│   │   │   ├── article_creator_agent_instructions.py    # NEW
│   │   │   ├── article_deployer_agent_instructions.py   # NEW
│   │   │   └── linkedin_sharer_agent_instructions.py    # NEW
│   │   ├── utils/               # Utility modules
│   │   │   └── repository_analyzer.py
│   │   └── agent.py             # Root orchestrator agent
│   └── publishing/              # Platform connectors
├── temp/                        # Temporary files
│   ├── github_clones/           # Cloned repositories
│   ├── article_drafts/          # Article drafts
│   └── github_pages/            # GitHub Pages deployment staging
├── .env.example                 # Environment variable template
├── pyproject.toml               # Project dependencies
└── README.md                    # This file
```

## Contributing

1.  Fork the repository.
2.  Create a feature branch.
3.  Commit your changes.
4.  Push to the branch.
5.  Open a Pull Request.
