"""Sokosumi MCP Server - Minimal wrapper for Sokosumi API"""

from typing import Any, Dict, List, Optional
import httpx
from mcp.server.fastmcp import FastMCP, Context
from mcp.server.session import ServerSession

# Base URLs
BASE_URLS = {
    "preprod": "https://preprod.sokosumi.com",
    "mainnet": "https://app.sokosumi.com"
}

# Initialize MCP server in stateless mode for multi-user support
mcp = FastMCP(
    name="Sokosumi API",
    instructions="Access to Sokosumi API. Tools are prefixed with 'preprod_' or 'mainnet_'. API key required via Authorization header.",
    stateless_http=True  # Enable stateless mode
)


def get_api_key(ctx: Context[ServerSession, None]) -> str:
    """Extract API key from Authorization header"""
    # The Authorization header should be available in the request context
    # In stateless HTTP mode, each request carries its own authorization
    try:
        # Try to get from session's request headers
        if hasattr(ctx.session, '_request_context'):
            headers = getattr(ctx.session._request_context, 'headers', {})
            auth_header = headers.get('Authorization', '')
            if auth_header.startswith('Bearer '):
                return auth_header[7:]
    except:
        pass
    
    # Fallback: try to get from request metadata
    try:
        if hasattr(ctx, 'request_context') and hasattr(ctx.request_context, 'meta'):
            meta = ctx.request_context.meta or {}
            if 'authorization' in meta:
                auth = meta['authorization']
                if auth.startswith('Bearer '):
                    return auth[7:]
    except:
        pass
    
    raise ValueError("API key required in Authorization header (format: 'Bearer YOUR_API_KEY')")


def get_client(api_key: str) -> httpx.Client:
    """Create HTTP client with API key header"""
    return httpx.Client(
        headers={"x-api-key": api_key},
        timeout=30.0
    )


# --- PREPROD Tools ---

@mcp.tool()
def preprod_get_user_info(ctx: Context[ServerSession, None]) -> Dict[str, Any]:
    """[Preprod] Get current user information"""
    api_key = get_api_key(ctx)
    with get_client(api_key) as client:
        response = client.get(f"{BASE_URLS['preprod']}/api/v1/users/me")
        response.raise_for_status()
        return response.json()


@mcp.tool()
def preprod_list_agents(ctx: Context[ServerSession, None]) -> List[Dict[str, Any]]:
    """[Preprod] List all available agents"""
    api_key = get_api_key(ctx)
    with get_client(api_key) as client:
        response = client.get(f"{BASE_URLS['preprod']}/api/v1/agents")
        response.raise_for_status()
        return response.json()


@mcp.tool()
def preprod_get_agent_jobs(agent_id: str, ctx: Context[ServerSession, None]) -> List[Dict[str, Any]]:
    """[Preprod] Get jobs for a specific agent
    
    Args:
        agent_id: The agent ID
    """
    api_key = get_api_key(ctx)
    with get_client(api_key) as client:
        response = client.get(f"{BASE_URLS['preprod']}/api/v1/agents/{agent_id}/jobs")
        response.raise_for_status()
        return response.json()


@mcp.tool()
def preprod_list_jobs(
    ctx: Context[ServerSession, None],
    status: Optional[str] = None,
    agent_id: Optional[str] = None
) -> List[Dict[str, Any]]:
    """[Preprod] List jobs with optional filters
    
    Args:
        status: Filter by job status (e.g., 'payment_pending')
        agent_id: Filter by agent ID
    """
    api_key = get_api_key(ctx)
    params = {}
    if status:
        params["status"] = status
    if agent_id:
        params["agentId"] = agent_id
    
    with get_client(api_key) as client:
        response = client.get(f"{BASE_URLS['preprod']}/api/v1/jobs", params=params)
        response.raise_for_status()
        return response.json()


@mcp.tool()
def preprod_get_agent_input_schema(agent_id: str, ctx: Context[ServerSession, None]) -> Dict[str, Any]:
    """[Preprod] Get input schema for a specific agent
    
    Args:
        agent_id: The agent ID
    """
    api_key = get_api_key(ctx)
    with get_client(api_key) as client:
        response = client.get(f"{BASE_URLS['preprod']}/api/v1/agents/{agent_id}/input-schema")
        response.raise_for_status()
        return response.json()


@mcp.tool()
def preprod_create_agent_job(
    agent_id: str,
    input_data: Dict[str, Any],
    max_accepted_credits: float,
    ctx: Context[ServerSession, None]
) -> Dict[str, Any]:
    """[Preprod] Create a new job for an agent
    
    Args:
        agent_id: The agent ID
        input_data: Input data for the job (agent-specific)
        max_accepted_credits: Maximum credits to spend
    """
    api_key = get_api_key(ctx)
    payload = {
        "inputData": input_data,
        "maxAcceptedCredits": max_accepted_credits
    }
    
    with get_client(api_key) as client:
        response = client.post(
            f"{BASE_URLS['preprod']}/api/v1/agents/{agent_id}/jobs",
            json=payload
        )
        response.raise_for_status()
        return response.json()


# --- MAINNET Tools ---

@mcp.tool()
def mainnet_get_user_info(ctx: Context[ServerSession, None]) -> Dict[str, Any]:
    """[Mainnet] Get current user information"""
    api_key = get_api_key(ctx)
    with get_client(api_key) as client:
        response = client.get(f"{BASE_URLS['mainnet']}/api/v1/users/me")
        response.raise_for_status()
        return response.json()


@mcp.tool()
def mainnet_list_agents(ctx: Context[ServerSession, None]) -> List[Dict[str, Any]]:
    """[Mainnet] List all available agents"""
    api_key = get_api_key(ctx)
    with get_client(api_key) as client:
        response = client.get(f"{BASE_URLS['mainnet']}/api/v1/agents")
        response.raise_for_status()
        return response.json()


@mcp.tool()
def mainnet_get_agent_jobs(agent_id: str, ctx: Context[ServerSession, None]) -> List[Dict[str, Any]]:
    """[Mainnet] Get jobs for a specific agent
    
    Args:
        agent_id: The agent ID
    """
    api_key = get_api_key(ctx)
    with get_client(api_key) as client:
        response = client.get(f"{BASE_URLS['mainnet']}/api/v1/agents/{agent_id}/jobs")
        response.raise_for_status()
        return response.json()


@mcp.tool()
def mainnet_list_jobs(
    ctx: Context[ServerSession, None],
    status: Optional[str] = None,
    agent_id: Optional[str] = None
) -> List[Dict[str, Any]]:
    """[Mainnet] List jobs with optional filters
    
    Args:
        status: Filter by job status (e.g., 'payment_pending')
        agent_id: Filter by agent ID
    """
    api_key = get_api_key(ctx)
    params = {}
    if status:
        params["status"] = status
    if agent_id:
        params["agentId"] = agent_id
    
    with get_client(api_key) as client:
        response = client.get(f"{BASE_URLS['mainnet']}/api/v1/jobs", params=params)
        response.raise_for_status()
        return response.json()


@mcp.tool()
def mainnet_get_agent_input_schema(agent_id: str, ctx: Context[ServerSession, None]) -> Dict[str, Any]:
    """[Mainnet] Get input schema for a specific agent
    
    Args:
        agent_id: The agent ID
    """
    api_key = get_api_key(ctx)
    with get_client(api_key) as client:
        response = client.get(f"{BASE_URLS['mainnet']}/api/v1/agents/{agent_id}/input-schema")
        response.raise_for_status()
        return response.json()


@mcp.tool()
def mainnet_create_agent_job(
    agent_id: str,
    input_data: Dict[str, Any],
    max_accepted_credits: float,
    ctx: Context[ServerSession, None]
) -> Dict[str, Any]:
    """[Mainnet] Create a new job for an agent
    
    Args:
        agent_id: The agent ID
        input_data: Input data for the job (agent-specific)
        max_accepted_credits: Maximum credits to spend
    """
    api_key = get_api_key(ctx)
    payload = {
        "inputData": input_data,
        "maxAcceptedCredits": max_accepted_credits
    }
    
    with get_client(api_key) as client:
        response = client.post(
            f"{BASE_URLS['mainnet']}/api/v1/agents/{agent_id}/jobs",
            json=payload
        )
        response.raise_for_status()
        return response.json()


# --- Server Info Tool ---

@mcp.tool()
def get_server_info() -> Dict[str, Any]:
    """Get information about the server configuration"""
    return {
        "environments": {
            "preprod": BASE_URLS["preprod"],
            "mainnet": BASE_URLS["mainnet"]
        },
        "authentication": "API key required via Authorization header (Bearer token)",
        "mode": "stateless"
    }


# Run server
if __name__ == "__main__":
    print("Starting Sokosumi MCP Server")
    print("Mode: Stateless (multi-user support)")
    print("Environments: preprod and mainnet")
    print("Authentication: Bearer token via Authorization header")
    print()
    print("Connect with Authorization header:")
    print('  "Authorization": "Bearer YOUR_API_KEY"')
    
    # Run with streamable HTTP transport on port 8000
    mcp.run(transport="streamable-http", port=8000)