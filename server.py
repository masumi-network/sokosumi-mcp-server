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


# --- PROMPTS ---

@mcp.prompt()
def select_agent_for_task(task_description: str, environment: str = "preprod") -> str:
    """Help user select the right agent for their task"""
    return f"""I'll help you select the right Sokosumi agent for your task.

Task: {task_description}
Environment: {environment}

Let me:
1. List available agents using {environment}_list_agents
2. Analyze which agents match your requirements
3. Show you the input schema for relevant agents
4. Recommend the best agent for your specific task

Starting by fetching available agents..."""


@mcp.prompt()
def create_job_wizard(agent_id: str, environment: str = "preprod") -> str:
    """Guide user through job creation process"""
    return f"""Let's create a job for agent {agent_id} on {environment}.

I'll guide you through:
1. Fetching the required input schema
2. Explaining each required field
3. Validating your input data format
4. Setting an appropriate credit limit
5. Submitting the job

First, let me get the input schema for this agent..."""


@mcp.prompt()
def monitor_jobs(status_filter: Optional[str] = None, environment: str = "preprod") -> str:
    """Set up job monitoring workflow"""
    status_info = f"Status filter: {status_filter}" if status_filter else "Showing all statuses"
    return f"""I'll help you monitor your Sokosumi jobs on {environment}.

{status_info}

I can:
1. List all current jobs and their statuses
2. Show detailed information for specific jobs
3. Track credit consumption across jobs
4. Filter by status (pending, running, completed, failed)
5. Check job results and outputs

Let me fetch your current jobs..."""


@mcp.prompt()
def troubleshoot_job(job_id: str, environment: str = "preprod") -> str:
    """Help debug a failed or stuck job"""
    return f"""Let's troubleshoot job {job_id} on {environment}.

I'll investigate:
1. Current job status and any error messages
2. Input data validation issues
3. Credit limit problems
4. Agent availability and compatibility
5. Historical success rate for similar jobs

Starting diagnostics now..."""


@mcp.prompt()
def estimate_job_cost(agent_id: str, job_count: int = 1, environment: str = "preprod") -> str:
    """Help estimate credits needed for jobs"""
    return f"""I'll help estimate the credit cost for running {job_count} job(s) on agent {agent_id}.

To provide an accurate estimate, I'll:
1. Check the agent's typical credit consumption
2. Review the input schema complexity
3. Consider the number of jobs you plan to run
4. Provide a recommended credit buffer

Environment: {environment}

Let me fetch the agent details and analyze credit requirements..."""


@mcp.prompt()
def quick_status_check(environment: str = "preprod") -> str:
    """Quick overview of all jobs and agents"""
    return f"""I'll give you a quick overview of your Sokosumi {environment} environment.

Checking:
1. Your user information and credit balance
2. Available agents and their status
3. Recent jobs (last 10)
4. Any failed or stuck jobs
5. Credit consumption trends

Gathering information now..."""


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