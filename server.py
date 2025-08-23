"""Sokosumi MCP Server - Minimal wrapper for Sokosumi API"""

import os
from typing import Any, Dict, List, Optional
import httpx
from mcp.server.fastmcp import FastMCP

# Base URLs
BASE_URLS = {
    "preprod": "https://preprod.sokosumi.com",
    "mainnet": "https://app.sokosumi.com"
}

# Initialize MCP server
mcp = FastMCP(
    name="Sokosumi API",
    instructions="Access to Sokosumi API. Tools are prefixed with 'preprod_' or 'mainnet_'. Requires SOKOSUMI_API_KEY environment variable."
)

# Get API key from environment
def get_api_key() -> str:
    """Get API key from environment variable"""
    api_key = os.getenv("SOKOSUMI_API_KEY", "")
    if not api_key:
        raise ValueError("SOKOSUMI_API_KEY environment variable is required")
    return api_key


def get_client() -> httpx.Client:
    """Create HTTP client with API key header"""
    return httpx.Client(
        headers={"x-api-key": get_api_key()},
        timeout=30.0
    )


# --- PREPROD Tools ---

@mcp.tool()
def preprod_get_user_info() -> Dict[str, Any]:
    """[Preprod] Get current user information"""
    with get_client() as client:
        response = client.get(f"{BASE_URLS['preprod']}/api/v1/users/me")
        response.raise_for_status()
        return response.json()


@mcp.tool()
def preprod_list_agents() -> List[Dict[str, Any]]:
    """[Preprod] List all available agents"""
    with get_client() as client:
        response = client.get(f"{BASE_URLS['preprod']}/api/v1/agents")
        response.raise_for_status()
        return response.json()


@mcp.tool()
def preprod_get_agent_jobs(agent_id: str) -> List[Dict[str, Any]]:
    """[Preprod] Get jobs for a specific agent
    
    Args:
        agent_id: The agent ID
    """
    with get_client() as client:
        response = client.get(f"{BASE_URLS['preprod']}/api/v1/agents/{agent_id}/jobs")
        response.raise_for_status()
        return response.json()


@mcp.tool()
def preprod_list_jobs(
    status: Optional[str] = None,
    agent_id: Optional[str] = None
) -> List[Dict[str, Any]]:
    """[Preprod] List jobs with optional filters
    
    Args:
        status: Filter by job status (e.g., 'payment_pending')
        agent_id: Filter by agent ID
    """
    params = {}
    if status:
        params["status"] = status
    if agent_id:
        params["agentId"] = agent_id
    
    with get_client() as client:
        response = client.get(f"{BASE_URLS['preprod']}/api/v1/jobs", params=params)
        response.raise_for_status()
        return response.json()


@mcp.tool()
def preprod_get_agent_input_schema(agent_id: str) -> Dict[str, Any]:
    """[Preprod] Get input schema for a specific agent
    
    Args:
        agent_id: The agent ID
    """
    with get_client() as client:
        response = client.get(f"{BASE_URLS['preprod']}/api/v1/agents/{agent_id}/input-schema")
        response.raise_for_status()
        return response.json()


@mcp.tool()
def preprod_create_agent_job(
    agent_id: str,
    input_data: Dict[str, Any],
    max_accepted_credits: float
) -> Dict[str, Any]:
    """[Preprod] Create a new job for an agent
    
    Args:
        agent_id: The agent ID
        input_data: Input data for the job (agent-specific)
        max_accepted_credits: Maximum credits to spend
    """
    payload = {
        "inputData": input_data,
        "maxAcceptedCredits": max_accepted_credits
    }
    
    with get_client() as client:
        response = client.post(
            f"{BASE_URLS['preprod']}/api/v1/agents/{agent_id}/jobs",
            json=payload
        )
        response.raise_for_status()
        return response.json()


# --- MAINNET Tools ---

@mcp.tool()
def mainnet_get_user_info() -> Dict[str, Any]:
    """[Mainnet] Get current user information"""
    with get_client() as client:
        response = client.get(f"{BASE_URLS['mainnet']}/api/v1/users/me")
        response.raise_for_status()
        return response.json()


@mcp.tool()
def mainnet_list_agents() -> List[Dict[str, Any]]:
    """[Mainnet] List all available agents"""
    with get_client() as client:
        response = client.get(f"{BASE_URLS['mainnet']}/api/v1/agents")
        response.raise_for_status()
        return response.json()


@mcp.tool()
def mainnet_get_agent_jobs(agent_id: str) -> List[Dict[str, Any]]:
    """[Mainnet] Get jobs for a specific agent
    
    Args:
        agent_id: The agent ID
    """
    with get_client() as client:
        response = client.get(f"{BASE_URLS['mainnet']}/api/v1/agents/{agent_id}/jobs")
        response.raise_for_status()
        return response.json()


@mcp.tool()
def mainnet_list_jobs(
    status: Optional[str] = None,
    agent_id: Optional[str] = None
) -> List[Dict[str, Any]]:
    """[Mainnet] List jobs with optional filters
    
    Args:
        status: Filter by job status (e.g., 'payment_pending')
        agent_id: Filter by agent ID
    """
    params = {}
    if status:
        params["status"] = status
    if agent_id:
        params["agentId"] = agent_id
    
    with get_client() as client:
        response = client.get(f"{BASE_URLS['mainnet']}/api/v1/jobs", params=params)
        response.raise_for_status()
        return response.json()


@mcp.tool()
def mainnet_get_agent_input_schema(agent_id: str) -> Dict[str, Any]:
    """[Mainnet] Get input schema for a specific agent
    
    Args:
        agent_id: The agent ID
    """
    with get_client() as client:
        response = client.get(f"{BASE_URLS['mainnet']}/api/v1/agents/{agent_id}/input-schema")
        response.raise_for_status()
        return response.json()


@mcp.tool()
def mainnet_create_agent_job(
    agent_id: str,
    input_data: Dict[str, Any],
    max_accepted_credits: float
) -> Dict[str, Any]:
    """[Mainnet] Create a new job for an agent
    
    Args:
        agent_id: The agent ID
        input_data: Input data for the job (agent-specific)
        max_accepted_credits: Maximum credits to spend
    """
    payload = {
        "inputData": input_data,
        "maxAcceptedCredits": max_accepted_credits
    }
    
    with get_client() as client:
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
        "api_key_configured": bool(os.getenv("SOKOSUMI_API_KEY"))
    }


# Run server
if __name__ == "__main__":
    api_key_configured = bool(os.getenv("SOKOSUMI_API_KEY"))
    
    print("Starting Sokosumi MCP Server")
    print("Environments: preprod and mainnet")
    print(f"API key configured: {api_key_configured}")
    
    if not api_key_configured:
        print("\nWARNING: SOKOSUMI_API_KEY environment variable not set!")
        print("Set it before connecting clients:")
        print("  export SOKOSUMI_API_KEY=your_api_key_here")
    
    # Run with streamable HTTP transport
    mcp.run(transport="streamable-http", port=8000)