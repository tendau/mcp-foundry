"""Azure AI Agent Service MCP Adapter"""

import os
import sys
import logging
from datetime import datetime, timedelta
from typing import Any, Optional, Tuple

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import MessageRole
from azure.identity import DefaultAzureCredential

# Configure logging - only essential information
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stderr,
)
logger = logging.getLogger("azure_agent_mcp")

# Create MCP server
mcp = FastMCP(
    "azure-agent",
    description="MCP adapter for Azure AI Agent Service integration",
    dependencies=["azure-identity", "python-dotenv", "azure-ai-projects"],
)


class AzureAgentAdapter:
    """Client for connecting to existing Azure AI Agents."""

    def __init__(self):
        """Initialize Azure AI Agent client with credentials from environment variables."""
        # Load environment variables
        self.project_connection_string = os.getenv("PROJECT_CONNECTION_STRING")
        self.default_agent_id = os.getenv("DEFAULT_AGENT_ID")

        # Validate essential environment variables
        if not self.project_connection_string:
            raise ValueError("Missing required environment variable: PROJECT_CONNECTION_STRING")

        # Initialize AIProjectClient
        try:
            self.client = AIProjectClient.from_connection_string(
                credential=DefaultAzureCredential(),
                conn_str=self.project_connection_string,
            )
        except Exception as e:
            logger.error(f"Failed to initialize AIProjectClient: {str(e)}")
            raise

        # Cache for agents and threads
        self._agent_cache = {}
        self._thread_cache = {}
        self._cache_expiry = {}

    async def _get_agent(self, agent_id: str) -> Any:
        """Get an agent by ID with caching."""
        now = datetime.now()

        # Check cache
        if agent_id in self._agent_cache:
            if now < self._cache_expiry.get(agent_id, now):
                return self._agent_cache[agent_id]

        # Fetch agent
        try:
            agent = self.client.agents.get_agent(agent_id=agent_id)

            # Cache agent for 1 hour
            self._agent_cache[agent_id] = agent
            self._cache_expiry[agent_id] = now + timedelta(hours=1)

            return agent
        except Exception as e:
            logger.error(f"Agent retrieval failed - ID: {agent_id}, Error: {str(e)}")
            raise ValueError(f"Agent not found or inaccessible: {agent_id}")

    async def _get_thread(self, thread_id: Optional[str] = None) -> Tuple[str, Any]:
        """Get a thread by ID or create a new one."""
        if thread_id and thread_id in self._thread_cache:
            return thread_id, self._thread_cache[thread_id]

        # Create new thread
        try:
            thread = self.client.agents.create_thread()
            thread_id = thread.id
            self._thread_cache[thread_id] = thread
            return thread_id, thread
        except Exception as e:
            logger.error(f"Thread creation failed: {str(e)}")
            raise

    async def query_agent(
        self, agent_id: str, query: str, thread_id: Optional[str] = None
    ) -> Tuple[str, str]:
        """
        Query an Azure AI Agent and get the response.

        Args:
            agent_id: The ID of the agent to query
            query: The question or request to send to the agent
            thread_id: Optional thread ID for continuation of conversation

        Returns:
            Tuple of (thread_id, response_text)
        """
        try:
            # Get or create agent and thread
            agent = await self._get_agent(agent_id)
            thread_id, thread = await self._get_thread(thread_id)

            # Add message to thread
            message = self.client.agents.create_message(
                thread_id=thread_id, role=MessageRole.USER, content=query
            )

            # Process the run
            run = self.client.agents.create_and_process_run(
                thread_id=thread_id, agent_id=agent_id
            )

            if run.status == "failed":
                error_msg = f"Agent run failed: {run.last_error}"
                logger.error(error_msg)
                return thread_id, f"Error: {error_msg}"

            # Get the agent's response
            response_message = self.client.agents.list_messages(
                thread_id=thread_id
            ).get_last_message_by_role(MessageRole.AGENT)

            result = ""
            citations = []

            if response_message:
                # Collect text content
                for text_message in response_message.text_messages:
                    result += text_message.text.value + "\n"

                # Collect citations
                for annotation in response_message.url_citation_annotations:
                    citation = f"[{annotation.url_citation.title}]({annotation.url_citation.url})"
                    if citation not in citations:
                        citations.append(citation)

            # Add citations if any
            if citations:
                result += "\n\n## Sources\n"
                for citation in citations:
                    result += f"- {citation}\n"

            return thread_id, result.strip()

        except Exception as e:
            logger.error(f"Agent query failed - ID: {agent_id}, Error: {str(e)}")
            raise


# Initialize Azure AI Agent adapter with proper error handling
try:
    agent_adapter = AzureAgentAdapter()
except Exception as e:
    logger.error(f"Adapter initialization failed: {str(e)}")
    agent_adapter = None


@mcp.tool()
async def connect_agent(agent_id: str, query: str, thread_id: str = None) -> str:
    """
    Connect to a specific Azure AI Agent.
    """
    if agent_adapter is None:
        return "Error: Azure AI Agent adapter is not initialized. Check server logs for details."

    try:
        thread_id, response = await agent_adapter.query_agent(
            agent_id, query, thread_id
        )
        return (
            f"## Response from Azure AI Agent\n\nThread ID: {thread_id}\n\n{response}"
        )
    except Exception as e:
        return f"Error connecting to agent: {str(e)}"


@mcp.tool()
async def query_default_agent(query: str, thread_id: str = None) -> str:
    """
    Send a query to the default configured Azure AI Agent.
    """
    if agent_adapter is None:
        return "Error: Azure AI Agent adapter is not initialized. Check server logs for details."

    if not agent_adapter.default_agent_id:
        return "Error: No default agent configured. Set DEFAULT_AGENT_ID environment variable or use connect_agent tool."

    try:
        thread_id, response = await agent_adapter.query_agent(
            agent_adapter.default_agent_id, query, thread_id
        )
        return f"## Response from Default Azure AI Agent\n\nThread ID: {thread_id}\n\n{response}"
    except Exception as e:
        return f"Error querying default agent: {str(e)}"


@mcp.tool()
async def list_agents() -> str:
    """
    List available agents in the Azure AI Agent Service.
    """
    if agent_adapter is None:
        return "Error: Azure AI Agent adapter is not initialized. Check server logs for details."
        
    try:
        agents = agent_adapter.client.agents.list_agents()
        if not agents or not agents.data:
            return "No agents found in the Azure AI Agent Service."
            
        result = "## Available Azure AI Agents\n\n"
        for agent in agents.data:
            result += f"- **{agent.name}**: `{agent.id}`\n"
            
        if agent_adapter.default_agent_id:
            result += f"\n**Default Agent ID**: `{agent_adapter.default_agent_id}`"
            
        return result
    except Exception as e:
        return f"Error listing agents: {str(e)}"


def main():
    """Run the MCP adapter."""
    # Load environment variables
    load_dotenv()

    # Run the server with stdio transport (default)
    mcp.run()


if __name__ == "__main__":
    main()