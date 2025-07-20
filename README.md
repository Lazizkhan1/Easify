# OyGul ERP Agent

A Python-based AI ERP agent for the OyGul flower shop platform that helps manage products through natural language interactions.

## Overview

This agent is built using Google's Agent Development Kit (ADK) and provides an intelligent interface for managing products within the OyGul flower shop. It can understand natural language queries to perform operations.

## Features

- **Product Management**: Create, retrieve, edit, and delete flowers and bouquets.
- **Natural Language Interface**: Interact with the ERP system using natural language queries.
- **Flexible Translations**: Supports multiple languages for product names and descriptions.

## Prerequisites

- Python 3.12 or higher
- [UV](https://docs.astral.sh/uv/) package manager (recommended, a fast Python package and dependency manager; see [UV documentation](https://docs.astral.sh/uv/))

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://gitlab.com/oy-gul/og-py-erp-agent.git
   cd og-py-erp-agent
   ```

2. **Set up a virtual environment**:
   ```bash
   uv venv
   ```

3. **Install dependencies**:
   ```bash
   uv sync
   ```

### Running the Agent (Console)

To run the agent in your console, execute the `main.py` file:

```bash
python main.py
```

This will start an interactive session where you can type your queries.

For more information about Google Agent Development Kit (ADK), visit the [official documentation](https://google.github.io/adk-docs/get-started/quickstart/).


## Project Structure

```
og-py-erp-agent/
├── main.py               # Main entry point for the console-based ERP agent
├── agents.py             # Defines the main ERP AI agent and its roles
├── tools/                # Contains custom tools used by the agents
│   └── content/          # Tools for interacting with the OyGul content management API
│       ├── feed.py       # General product search tool (can be used for various product types)
│       ├── flowers.py    # Tools for managing flower products (create, get, edit, delete)
│       └── bouquets.py   # Tools for managing bouquet products (create, get, edit, delete)
├── utils/                # Utility functions
│   └── call_agent.py     # Helper for asynchronously calling agents
├── examples/             # Example interactions or scripts (if any)
├── pyproject.toml        # Project configuration and dependencies
├── uv.lock               # Locked dependency versions
├── .python-version       # Python version specification
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

## Dependencies

- **google-adk**: Google's Agent Development Kit for building AI agents
- **litellm**: LiteLLM for model integration
- **requests**: HTTP library for API calls


## Development

### Adding New Tools

To add new functionality to the agent, create new functions and add them to the `tools` list in the `root_erp_agent` configuration in `agents.py`:

```python
def new_tool_function(param1: str, param2: int) -> dict:
    """Description of what this tool does."""
    # Implementation here
    return {"status": "success", "data": result}

root_erp_agent = Agent(
    # ... existing configuration ...
    tools=[create_flower, get_flower_types, new_tool_function],
)
```
"# Easify" 
