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
    instructions="Access to Sokosumi API. Tools are prefixed with 'preprod_' or 'mainnet_'. Configure API key using 'configure_api_key' tool first."
)

# Store API key (can be set via environment or configure tool)
API_KEY: str = os.getenv("SOKOSUMI_API_KEY", "")

# HTTP client factory
def get_client(api_key: Optional[str] = None) -> httpx.Client:
    """Create HTTP client with API key header"""
    key = api_key or API_KEY
    if not key:
        raise ValueError("API key not configured. Use 'configure_api_key' tool or set SOKOSUMI_API_KEY environment variable.")
    return httpx.Client(
        headers={"x-api-key": key},
        timeout=30.0
    )


# --- Configuration Tool ---

@mcp.tool()
def configure_api_key(api_key: str) -> Dict[str, str]:
    """Configure API key for Sokosumi API access
    
    Args:
        api_key: Your Sokosumi API key
    """
    global API_KEY
    API_KEY = api_key
    return {"status": "configured", "message": "API key set successfully"}


@mcp.tool()
def get_configuration() -> Dict[str, Any]:
    """Get current server configuration"""
    return {
        "api_key_configured": bool(API_KEY),
        "environments": {
            "preprod": BASE_URLS["preprod"],
            "mainnet": BASE_URLS["mainnet"]
        }
    }


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


# Run server
if __name__ == "__main__":
    print("Starting Sokosumi MCP Server")
    print("Environments: preprod and mainnet")
    print(f"API key configured: {bool(API_KEY)}")
    if not API_KEY:
        print("Note: Configure API key using 'configure_api_key' tool or SOKOSUMI_API_KEY env var")
    
    # Run with streamable HTTP transport only
    mcp.run(transport="streamable-http", port=8000)