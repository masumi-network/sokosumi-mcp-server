# Sokosumi MCP Server

A minimal MCP (Model Context Protocol) server that provides access to the Sokosumi API.

## Features

- Streamable HTTP transport only
- Stateless mode for multi-user support
- Support for both preprod and mainnet environments (as separate tool sets)
- API key authentication via Authorization header
- Clean, minimal implementation

## Available Features

### Prompts (Guided Workflows)
- `select_agent_for_task(task_description, environment)` - Help select the right agent for a task
- `create_job_wizard(agent_id, environment)` - Guide through job creation process
- `monitor_jobs(status_filter?, environment)` - Set up job monitoring workflow
- `troubleshoot_job(job_id, environment)` - Debug failed or stuck jobs
- `estimate_job_cost(agent_id, job_count, environment)` - Estimate credits needed
- `quick_status_check(environment)` - Quick overview of jobs and agents

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

## Authentication

The server runs in stateless mode and extracts the API key from the Authorization header of each request. Each user connects with their own API key.

### MCP Client Configuration

Configure your MCP client with the Authorization header:

```json
{
  "mcpServers": {
    "sokosumi": {
      "type": "http",
      "url": "http://localhost:8000/mcp",
      "headers": {
        "Authorization": "Bearer YOUR_API_KEY_HERE"
      }
    }
  }
}
```

### Python Client Example

```python
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

# Configure headers with your API key
headers = {
    "Authorization": "Bearer YOUR_API_KEY_HERE"
}

async with streamablehttp_client(
    "http://localhost:8000/mcp",
    headers=headers
) as (read, write, _):
    async with ClientSession(read, write) as session:
        await session.initialize()
        
        # List available tools
        tools = await session.list_tools()
        
        # Call preprod tools
        result = await session.call_tool("preprod_get_user_info")
        
        # Call mainnet tools
        result = await session.call_tool("mainnet_list_agents")
```

## Deployment

### Local Development
```bash
python server.py
```

### Docker Deployment
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt server.py ./
RUN pip install -r requirements.txt
EXPOSE 8000
CMD ["python", "server.py"]
```

### Cloud Deployment

Deploy as a containerized service. The server is stateless and can scale horizontally.

## Base URLs

- Preprod: `https://preprod.sokosumi.com`
- Mainnet: `https://app.sokosumi.com`

## How It Works

1. Start the server once - it runs stateless and supports multiple users
2. Each user connects with their own API key in the Authorization header
3. The server extracts the API key from each request and uses it for Sokosumi API calls
4. Multiple users can connect simultaneously, each with their own API key

## Testing

Test the server with the MCP Inspector:
```bash
uv run mcp dev server.py
```

Note: When testing with MCP Inspector, you'll need to configure the Authorization header with your API key.

## Security Notes

- Never commit API keys to version control
- Each user's API key is isolated to their own requests
- The server doesn't store any API keys
- For production, deploy behind HTTPS