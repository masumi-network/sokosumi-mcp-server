# Sokosumi MCP Server

A minimal MCP (Model Context Protocol) server that provides access to the Sokosumi API.

## Features

- Streamable HTTP transport only
- Support for both preprod and mainnet environments (as separate tool sets)
- API key authentication via environment variable
- Clean, minimal implementation
- Simple deployment model

## Available Tools

### Server Info
- `get_server_info()` - Get server configuration and available environments

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

# Set API key
export SOKOSUMI_API_KEY=your_api_key_here

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

# Set API key
export SOKOSUMI_API_KEY=your_api_key_here

# Run the server
python server.py
```

The server will start on `http://localhost:8000/mcp`

## Authentication

The server uses environment variable authentication for simplicity. Each server instance uses one API key.

### Single-User Setup

Set the API key as an environment variable:
```bash
export SOKOSUMI_API_KEY=your_api_key_here
python server.py
```

### Multi-User Setup

For multiple users with different API keys, run separate server instances on different ports:

**User 1 (port 8000):**
```bash
SOKOSUMI_API_KEY=user1_api_key python server.py
```

**User 2 (port 8001):**
```bash
SOKOSUMI_API_KEY=user2_api_key python -c "
from server import mcp
mcp.run(transport='streamable-http', port=8001)
"
```

## Client Configuration

### MCP Client Configuration

Configure your MCP client to connect to the server:

```json
{
  "mcpServers": {
    "sokosumi": {
      "type": "http",
      "url": "http://localhost:8000/mcp"
    }
  }
}
```

### Python Client Example

```python
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

async with streamablehttp_client("http://localhost:8000/mcp") as (read, write, _):
    async with ClientSession(read, write) as session:
        await session.initialize()
        
        # List available tools
        tools = await session.list_tools()
        
        # Call preprod tools
        result = await session.call_tool("preprod_get_user_info")
        
        # Call mainnet tools
        result = await session.call_tool("mainnet_list_agents")
```

## Deployment Options

### Local Development
```bash
export SOKOSUMI_API_KEY=your_api_key
python server.py
```

### Docker Deployment
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt server.py ./
RUN pip install -r requirements.txt
ENV SOKOSUMI_API_KEY=${SOKOSUMI_API_KEY}
CMD ["python", "server.py"]
```

### Cloud Deployment

Deploy as a containerized service with the API key set as an environment variable in your cloud platform's secret management system.

## Base URLs

- Preprod: `https://preprod.sokosumi.com`
- Mainnet: `https://app.sokosumi.com`

## Testing

Test the server with the MCP Inspector:
```bash
export SOKOSUMI_API_KEY=your_api_key
uv run mcp dev server.py
```

## Security Notes

- Never commit API keys to version control
- Use environment variables or secret management systems
- For production, deploy behind HTTPS
- Each server instance handles one API key (one user)