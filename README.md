# Sokosumi MCP Server

A minimal MCP (Model Context Protocol) server that provides access to the Sokosumi API.

## Features

- Streamable HTTP transport only
- Support for both preprod and mainnet environments
- API key authentication
- Clean, minimal implementation

## Available Tools

- `get_user_info()` - Get current user information
- `list_agents()` - List all available agents
- `get_agent_jobs(agent_id)` - Get jobs for a specific agent
- `list_jobs(status?, agent_id?)` - List jobs with optional filters
- `get_agent_input_schema(agent_id)` - Get input schema for an agent
- `create_agent_job(agent_id, input_data, max_accepted_credits)` - Create a new agent job
- `get_server_info()` - Get server configuration info

## Setup

1. Install dependencies:
```bash
uv add "mcp[cli]" httpx python-dotenv
# or
pip install "mcp[cli]" httpx python-dotenv
```

2. Configure environment:
```bash
cp .env.example .env
# Edit .env and add your API key and environment
```

3. Run the server:
```bash
python server.py
# or
uv run server.py
```

The server will start on `http://localhost:8000/mcp`

## Environment Variables

- `SOKOSUMI_API_KEY` - Your Sokosumi API key (required)
- `SOKOSUMI_ENV` - Environment: 'preprod' or 'mainnet' (default: 'preprod')

## Base URLs

- Preprod: `https://preprod.sokosumi.com`
- Mainnet: `https://app.sokosumi.com`

## Client Connection

Connect to the server using the MCP streamable HTTP transport:

```python
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

async with streamablehttp_client("http://localhost:8000/mcp") as (read, write, _):
    async with ClientSession(read, write) as session:
        await session.initialize()
        
        # List available tools
        tools = await session.list_tools()
        
        # Call a tool
        result = await session.call_tool("get_user_info")
```

## Testing

Test the server with the MCP Inspector:
```bash
uv run mcp dev server.py
```
