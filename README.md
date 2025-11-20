# Knowledge Flow Agent

The **Knowledge Flow Agent** is an AI-powered developer advocate assistant designed to help you share your technical learnings with the community. It automates the process of researching topics, analyzing code repositories, and summarizing blog posts to generate content for platforms like GitHub Pages and LinkedIn.

Built with [Google's Agent Development Kit (ADK)](https://github.com/google/adk) and Python.

## Features

- **Orchestrator Agent**: Intelligently routes user requests to the appropriate tools.
- **GitHub Reader**: Analyzes GitHub repositories to understand code structure and content.
- **Blog Reader**: Scrapes and summarizes technical blog posts.
- **Topic Researcher**: Performs web searches to gather context on technical topics.
- **Multi-Platform Support**: (In Progress) Generates content tailored for GitHub Pages and LinkedIn.

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
    Edit `.env` and add your `GOOGLE_API_KEY`:
    ```
    GOOGLE_API_KEY=your_api_key_here
    ```

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
│   │   ├── tools/              # Sub-agent logic and tools
│   │   │   ├── github_reader.py
│   │   │   ├── blog_reader.py
│   │   │   └── topic_researcher.py
│   │   ├── prompts/            # System prompts
│   │   │   └── instructions.py
│   │   └── agent.py            # Main agent entry point
│   └── publishing/             # (Planned) Platform connectors
├── .env.example                # Environment variable template
├── pyproject.toml              # Project dependencies
└── README.md                   # This file
```

## Contributing

1.  Fork the repository.
2.  Create a feature branch.
3.  Commit your changes.
4.  Push to the branch.
5.  Open a Pull Request.
