"""Azure AI Agent Service MCP Server"""

import os
import sys
import logging
from datetime import datetime, timedelta
from typing import Optional, Tuple

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP, Context
from azure.ai.projects.aio import AIProjectClient
from azure.ai.projects.models import MessageRole, Agent, AgentThread
from azure.identity.aio import DefaultAzureCredential

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
    description="MCP server for Azure AI Agent Service integration",
    dependencies=["azure-identity", "python-dotenv", "azure-ai-projects"],
)


class AzureAgentServer:
    """Client for connecting to existing Azure AI Agents."""

    def __init__(self):
        """Initialize basic properties of the Azure Agent Server."""
        # Load environment variables
        self.project_connection_string = os.getenv("PROJECT_CONNECTION_STRING")
        self.default_agent_id = os.getenv("DEFAULT_AGENT_ID")

        # Validate essential environment variables
        if not self.project_connection_string:
            raise ValueError(
                "Missing required environment variable: PROJECT_CONNECTION_STRING"
            )

        # Placeholders that will be set during async initialization
        self.credential = None
        self.client = None

        # Cache for agents and threads
        self._agent_cache = {}
        self._cache_expiry = {}
        self._thread_cache = {}  # Maps client_id -> thread_id -> thread

    @classmethod
    async def create(cls):
        """Factory method for async initialization of the server."""
        server = cls()
        await server.initialize()
        return server

    async def initialize(self):
        """Asynchronously initialize the client connection."""
        try:
            self.credential = DefaultAzureCredential()
            self.client = AIProjectClient.from_connection_string(
                credential=self.credential,
                conn_str=self.project_connection_string,
            )
        except Exception as e:
            logger.error(f"Failed to initialize AIProjectClient: {str(e)}")
            raise

    async def _get_agent(self, agent_id: str) -> Agent:
        """Get an agent by ID with caching."""
        # #FEEDBACK: Method is declared async but has no awaits
        now = datetime.now()

        # Check cache
        if agent_id in self._agent_cache:
            if now < self._cache_expiry.get(agent_id, now):
                return self._agent_cache[agent_id]

        # Fetch agent
        try:
            # #FEEDBACK: Using proper async client method
            agent = await self.client.agents.get_agent(agent_id=agent_id)

            # Cache agent for 1 hour
            self._agent_cache[agent_id] = agent
            self._cache_expiry[agent_id] = now + timedelta(hours=1)

            return agent
        except Exception as e:
            logger.error(f"Agent retrieval failed - ID: {agent_id}, Error: {str(e)}")
            raise ValueError(f"Agent not found or inaccessible: {agent_id}")

    async def _get_thread(
        self, client_id: str, thread_id: Optional[str] = None
    ) -> Tuple[str, AgentThread]:
        """Get a thread by ID or create a new one with proper client isolation.

        Args:
            client_id: Unique identifier for the client session
            thread_id: Optional thread ID for continuation of conversation

        Note: Each client interaction is isolated through client_id to maintain separation:
        1. Creates natural conversation history for each client session
        2. Isolates interactions between different client sessions
        3. Preserves state within a single client conversation
        """
        # Initialize client's thread cache if not exists
        if client_id not in self._thread_cache:
            self._thread_cache[client_id] = {}

        # Return existing thread if provided and exists
        if thread_id and thread_id in self._thread_cache[client_id]:
            return thread_id, self._thread_cache[client_id][thread_id]

        # Create new thread
        try:
            thread = await self.client.agents.create_thread()
            thread_id = thread.id
            self._thread_cache[client_id][thread_id] = thread
            return thread_id, thread
        except Exception as e:
            logger.error(f"Thread creation failed: {str(e)}")
            raise

    async def query_agent(
        self, agent_id: str, query: str, client_id: str, thread_id: Optional[str] = None
    ) -> Tuple[str, str]:
        """
        Query an Azure AI Agent and get the response.

        Args:
            agent_id: The ID of the agent to query
            query: The question or request to send to the agent
            client_id: Unique identifier for the client session
            thread_id: Optional thread ID for continuation of conversation

        Returns:
            Tuple of (thread_id, response_text)
        """
        try:
            # Get or create agent and thread
            agent = await self._get_agent(agent_id)
            thread_id, thread = await self._get_thread(client_id, thread_id)

            # Add message to thread
            message = await self.client.agents.create_message(
                thread_id=thread_id, role=MessageRole.USER, content=query
            )

            # Process the run asynchronously
            run = await self.client.agents.create_run(
                thread_id=thread_id, agent_id=agent_id
            )

            # Poll until the run is complete
            while run.status in ["queued", "in_progress", "requires_action"]:
                await asyncio.sleep(1)  # Non-blocking sleep
                run = await self.client.agents.get_run(
                    thread_id=thread_id, run_id=run.id
                )

            if run.status == "failed":
                error_msg = f"Agent run failed: {run.last_error}"
                logger.error(error_msg)
                return thread_id, f"Error: {error_msg}"

            # Get the agent's response
            response_messages = await self.client.agents.list_messages(
                thread_id=thread_id
            )
            response_message = response_messages.get_last_message_by_role(
                MessageRole.AGENT
            )

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


# Initialize Azure AI Agent server with proper error handling
agent_server = None


async def initialize_server():
    """Initialize the Azure AI Agent server asynchronously."""
    global agent_server
    try:
        agent_server = await AzureAgentServer.create()
    except Exception as e:
        logger.error(f"Server initialization failed: {str(e)}")
        agent_server = None


@mcp.tool()
async def connect_agent(
    agent_id: str, query: str, thread_id: str = None, ctx: Context = None
) -> str:
    """
    Connect to a specific Azure AI Agent.
    """
    if agent_server is None:
        return "Error: Azure AI Agent server is not initialized. Check server logs for details."

    if ctx is None:
        return "Error: Request context is not available."

    # Use the request_id from the provided context as the client identifier
    client_id = f"client-{ctx.request_id}"

    try:
        thread_id, response = await agent_server.query_agent(
            agent_id, query, client_id, thread_id
        )
        return (
            f"## Response from Azure AI Agent\n\nThread ID: {thread_id}\n\n{response}"
        )
    except Exception as e:
        await ctx.error(f"Agent error: {str(e)}")  # Log error to client
        return f"Error connecting to agent: {str(e)}"


@mcp.tool()
async def query_default_agent(
    query: str, thread_id: str = None, ctx: Context = None
) -> str:
    """
    Send a query to the default configured Azure AI Agent.
    """
    if agent_server is None:
        return "Error: Azure AI Agent server is not initialized. Check server logs for details."

    if not agent_server.default_agent_id:
        return "Error: No default agent configured. Set DEFAULT_AGENT_ID environment variable or use connect_agent tool."

    if ctx is None:
        return "Error: Request context is not available."

    # Use the request_id from the provided context
    client_id = f"client-{ctx.request_id}"

    try:
        thread_id, response = await agent_server.query_agent(
            agent_server.default_agent_id, query, client_id, thread_id
        )
        return f"## Response from Default Azure AI Agent\n\nThread ID: {thread_id}\n\n{response}"
    except Exception as e:
        await ctx.error(f"Agent error: {str(e)}")  # Log error to client
        return f"Error querying default agent: {str(e)}"


@mcp.tool()
async def list_agents() -> str:
    """
    List available agents in the Azure AI Agent Service.
    """
    if agent_server is None:
        return "Error: Azure AI Agent server is not initialized. Check server logs for details."

    try:
        agents = await agent_server.client.agents.list_agents()
        if not agents or not agents.data:
            return "No agents found in the Azure AI Agent Service."

        result = "## Available Azure AI Agents\n\n"
        for agent in agents.data:
            result += f"- **{agent.name}**: `{agent.id}`\n"

        if agent_server.default_agent_id:
            result += f"\n**Default Agent ID**: `{agent_server.default_agent_id}`"

        return result
    except Exception as e:
        return f"Error listing agents: {str(e)}"


async def main():
    """Run the MCP server."""
    # Load environment variables
    load_dotenv()
    # Initialize the server asynchronously
    await initialize_server()


if __name__ == "__main__":
    import asyncio

    asyncio.run(initialize_server())
    mcp.run()
