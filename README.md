# Sokosumi MCP Server

A minimal MCP (Model Context Protocol) server that provides access to the Sokosumi API.

## Features

- Streamable HTTP transport only
- Support for both preprod and mainnet environments (as separate tool sets)
- API key configuration via tool or environment variable
- Clean, minimal implementation

## Available Tools

### Configuration Tools
- `configure_api_key(api_key)` - Configure API key for Sokosumi API access
- `get_configuration()` - Get current server configuration

### Preprod Tools (prefix: `preprod_`)
- `preprod_get_user_info()` - Get current user information
- `preprod_list_agents()` - List all available agents
- `preprod_get_agent_jobs(agent_id)` - Get jobs for a specific agent
- `preprod_list_jobs(status?, agent_id?)` - List jobs with optional filters
- `preprod_get_agent_input_schema(agent_id)` - Get input schema for an agent
- `preprod_create_agent_job(agent_id, input_data, max_accepted_credits)` - Create a new agent job

### Mainnet Tools (prefix: `mainnet_`)
- `mainnet_get_user_info()` - Get current user information
- `mainnet_list_agents()` - List all available agents
- `mainnet_get_agent_jobs(agent_id)` - Get jobs for a specific agent
- `mainnet_list_jobs(status?, agent_id?)` - List jobs with optional filters
- `mainnet_get_agent_input_schema(agent_id)` - Get input schema for an agent
- `mainnet_create_agent_job(agent_id, input_data, max_accepted_credits)` - Create a new agent job

## Setup

### Option 1: Using uv (Recommended)
```bash
# Install dependencies
uv add "mcp[cli]" httpx

# Run the server
uv run server.py
```

### Option 2: Using venv and pip
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the server
python server.py
```

The server will start on `http://localhost:8000/mcp`

## API Key Configuration

You have two options for configuring the API key:

### Option 1: Use the configure_api_key tool (Recommended)
After connecting to the server, call the `configure_api_key` tool with your API key:
```python
await session.call_tool("configure_api_key", {"api_key": "your_api_key_here"})
```

### Option 2: Environment Variable
Set the `SOKOSUMI_API_KEY` environment variable before starting the server:
```bash
export SOKOSUMI_API_KEY=your_api_key_here
python server.py
```

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
        
        # Configure API key
        await session.call_tool("configure_api_key", {"api_key": "your_api_key_here"})
        
        # List available tools
        tools = await session.list_tools()
        
        # Call preprod tools
        result = await session.call_tool("preprod_get_user_info")
        
        # Call mainnet tools
        result = await session.call_tool("mainnet_list_agents")
```

## Testing

Test the server with the MCP Inspector:
```bash
uv run mcp dev server.py
```