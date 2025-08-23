# MCP Python SDK Reference Summary

## Overview
The Model Context Protocol (MCP) Python SDK provides a standardized way for applications to provide context to LLMs. It enables building both MCP clients and servers with support for resources, tools, prompts, and various transport protocols.

## Installation
```bash
# Using uv (recommended)
uv add "mcp[cli]"

# Using pip
pip install "mcp[cli]"
```

## Core Components

### 1. FastMCP Server
The high-level interface for building MCP servers quickly:

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("ServerName")
```

### 2. Tools
Functions that LLMs can execute with side effects:
- Use `@mcp.tool()` decorator
- Support for structured output (Pydantic models, TypedDicts, dataclasses)
- Can receive Context for advanced operations
- Return types automatically determine structured vs unstructured output

### 3. Resources
Data endpoints similar to GET requests:
- Use `@mcp.resource("uri://pattern")` decorator
- Should not have side effects
- Support dynamic URI patterns

### 4. Prompts
Reusable templates for LLM interactions:
- Use `@mcp.prompt()` decorator
- Can return strings or Message objects
- Support for user/assistant message patterns

### 5. Context Object
Automatically injected into functions via type hints:
- Logging capabilities (debug, info, warning, error)
- Progress reporting
- Resource reading
- User elicitation
- LLM sampling
- Access to session, request metadata, and lifespan resources

## Transport Options

### Stdio (Default)
Standard input/output communication for desktop integrations

### Streamable HTTP (Recommended for Production)
- Stateful and stateless modes
- Better scalability
- Support for mounting in existing ASGI apps
- Default path: `/mcp`

### SSE (Being Superseded)
Server-sent events transport
- Default path: `/sse`

## Running Servers

### Development Mode
```bash
uv run mcp dev server.py
```

### Claude Desktop Integration
```bash
uv run mcp install server.py
```

### Direct Execution
```python
if __name__ == "__main__":
    mcp.run()
```

### ASGI Mounting
```python
from starlette.applications import Starlette
from starlette.routing import Mount

app = Starlette(
    routes=[
        Mount("/", app=mcp.streamable_http_app()),
    ]
)
```

## Advanced Features

### Lifespan Management
Initialize resources on startup, clean up on shutdown:
```python
@asynccontextmanager
async def app_lifespan(server: FastMCP):
    # Startup
    db = await Database.connect()
    yield {"db": db}
    # Shutdown
    await db.disconnect()

mcp = FastMCP("App", lifespan=app_lifespan)
```

### Authentication
OAuth 2.1 resource server support:
- TokenVerifier protocol implementation
- RFC 9728 Protected Resource Metadata
- Authorization Server discovery

### Structured Output
Tools automatically handle:
- Pydantic models
- TypedDicts
- Dataclasses with type hints
- Primitive types (wrapped in {"result": value})
- Lists and generic types

### Completions
Provide suggestions for prompt arguments and resource parameters based on context

### Elicitation
Request additional information from users during execution:
```python
result = await ctx.elicit(message, schema=PydanticModel)
```

### Sampling
Tools can request LLM text generation:
```python
result = await ctx.session.create_message(messages, max_tokens)
```

## Client Development

### Basic Client
```python
from mcp import ClientSession
from mcp.client.stdio import stdio_client

async with stdio_client(server_params) as (read, write):
    async with ClientSession(read, write) as session:
        await session.initialize()
        # Use session methods
```

### Available Client Methods
- `list_tools()`, `call_tool()`
- `list_resources()`, `read_resource()`
- `list_prompts()`, `get_prompt()`
- `complete()` for argument completions

## Project Structure Best Practice
```
mcp-server/
├── src/
│   ├── __init__.py
│   ├── server.py          # Main server
│   ├── handlers/          # Request handlers
│   ├── tools/            # Tool implementations
│   └── utils/            # Utilities
├── tests/
├── pyproject.toml
├── README.md
└── .env.example
```

## Testing Commands
```bash
ruff check .       # Linting
mypy src/         # Type checking
pytest            # Run tests
ruff format .     # Format code
```

## Key Primitives Summary

| Primitive | Control | Use Case |
|-----------|---------|----------|
| Prompts | User-controlled | Interactive templates (slash commands) |
| Resources | Application-controlled | Contextual data (files, API responses) |
| Tools | Model-controlled | Actions and computations |

## Important Notes
- Always use async/await for non-blocking operations
- Validate inputs/outputs according to MCP schemas
- Handle errors gracefully
- Use environment variables for configuration
- Never hardcode credentials
- Tools with side effects should be clearly documented
- Resources should be idempotent (no side effects)