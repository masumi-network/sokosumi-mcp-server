"""Sokosumi MCP Server - Minimal wrapper for Sokosumi API"""

import os
from typing import Any, Dict, List, Optional
import httpx
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

# Load environment variables
load_dotenv()

# Configuration
API_KEY = os.getenv("SOKOSUMI_API_KEY", "")
ENVIRONMENT = os.getenv("SOKOSUMI_ENV", "preprod").lower()

# Base URLs
BASE_URLS = {
    "preprod": "https://preprod.sokosumi.com",
    "mainnet": "https://app.sokosumi.com"
}

if ENVIRONMENT not in BASE_URLS:
    raise ValueError(f"Invalid environment: {ENVIRONMENT}. Must be 'preprod' or 'mainnet'")

BASE_URL = BASE_URLS[ENVIRONMENT]

# Initialize MCP server
mcp = FastMCP(
    name="Sokosumi API",
    instructions=f"Access to Sokosumi API ({ENVIRONMENT}). All requests require API key authentication."
)

# HTTP client with default headers
def get_client() -> httpx.Client:
    """Create HTTP client with API key header"""
    return httpx.Client(
        headers={"x-api-key": API_KEY},
        timeout=30.0
    )


# --- GET Tools ---

@mcp.tool()
def get_user_info() -> Dict[str, Any]:
    """Get current user information"""
    with get_client() as client:
        response = client.get(f"{BASE_URL}/api/v1/users/me")
        response.raise_for_status()
        return response.json()


@mcp.tool()
def list_agents() -> List[Dict[str, Any]]:
    """List all available agents"""
    with get_client() as client:
        response = client.get(f"{BASE_URL}/api/v1/agents")
        response.raise_for_status()
        return response.json()


@mcp.tool()
def get_agent_jobs(agent_id: str) -> List[Dict[str, Any]]:
    """Get jobs for a specific agent
    
    Args:
        agent_id: The agent ID
    """
    with get_client() as client:
        response = client.get(f"{BASE_URL}/api/v1/agents/{agent_id}/jobs")
        response.raise_for_status()
        return response.json()


@mcp.tool()
def list_jobs(
    status: Optional[str] = None,
    agent_id: Optional[str] = None
) -> List[Dict[str, Any]]:
    """List jobs with optional filters
    
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
        response = client.get(f"{BASE_URL}/api/v1/jobs", params=params)
        response.raise_for_status()
        return response.json()


@mcp.tool()
def get_agent_input_schema(agent_id: str) -> Dict[str, Any]:
    """Get input schema for a specific agent
    
    Args:
        agent_id: The agent ID
    """
    with get_client() as client:
        response = client.get(f"{BASE_URL}/api/v1/agents/{agent_id}/input-schema")
        response.raise_for_status()
        return response.json()


# --- POST Tools ---

@mcp.tool()
def create_agent_job(
    agent_id: str,
    input_data: Dict[str, Any],
    max_accepted_credits: float
) -> Dict[str, Any]:
    """Create a new job for an agent
    
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
            f"{BASE_URL}/api/v1/agents/{agent_id}/jobs",
            json=payload
        )
        response.raise_for_status()
        return response.json()


# --- Server Info Tool ---

@mcp.tool()
def get_server_info() -> Dict[str, str]:
    """Get information about the current server configuration"""
    return {
        "environment": ENVIRONMENT,
        "base_url": BASE_URL,
        "api_key_configured": bool(API_KEY)
    }


# Run server
if __name__ == "__main__":
    if not API_KEY:
        print("WARNING: SOKOSUMI_API_KEY not set in environment")
    
    print(f"Starting Sokosumi MCP Server")
    print(f"Environment: {ENVIRONMENT}")
    print(f"Base URL: {BASE_URL}")
    
    # Run with streamable HTTP transport only
    mcp.run(transport="streamable-http", port=8000)