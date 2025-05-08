from mcp.server.fastmcp import FastMCP, Context
from dotenv import load_dotenv
import requests
import os

load_dotenv()

mcp = FastMCP("azure-ai-foundry-labs-mcp-server")
labs_api_url = os.environ.get("LABS_API_URL", "https://labs-mcp-api.azurewebsites.net//api/v1")
server_name = os.environ.get("SERVER_NAME", "azure-ai-foundry-labs-mcp-server")
server_version = os.environ.get("SERVER_VERSION", "0.0.1")

def get_client_headers_info(ctx):
    """Get client headers info."""
    client_info = getattr(getattr(ctx.session._client_params, "clientInfo", None), "__dict__", {}) or {}
    client_name = client_info.get("name", "UnknownClient").replace(" ", "-")
    client_version = client_info.get("version", "0.0.0")

    headers = {
        "User-Agent": f"MCP-Client/{client_name} - {client_version}",
        "X-MCP-Server": f"{server_name}/{server_version}",
    }
    return headers

@mcp.tool()
async def get_azure_ai_foundry_labs_projects_list(ctx: Context) -> str:
    """Get a list of all supported projects from Azure AI Foundry Labs."""

    headers = get_client_headers_info(ctx)

    response = requests.get(f"{labs_api_url}/projects?source=afl", headers=headers)
    if response.status_code != 200:
        return f"Error fetching projects from API: {response.status_code}"

    project_reponse = response.json()

    return project_reponse["projects"]

@mcp.tool()
async def get_implementation_details_for_labs_project(project_name: str, ctx: Context) -> str:
    """
    Detailed usage guidance (scripts, docs, etc) on how to implement a particular project from GitHub Models.
    Use this tool to get the implementation details of a project.
    Do not assume you know how to implement a project just because you know the project name.

    Args:
        project_name: name of project
    """

    headers = get_client_headers_info(ctx)

    response = requests.get(f"{labs_api_url}/projects/{project_name}/implementation", headers=headers)
    if response.status_code != 200:
        return f"Error fetching projects from API: {response.status_code}"

    project_response = response.json()

    return project_response


@mcp.tool()
def get_foundry_copilot_instructions(ctx: Context) -> str:
    """Get instructions for using Foundry Copilot.
    Only call this when someone asks for help using Foundry models or Foundry Labs."""

    headers = get_client_headers_info(ctx)

    response = requests.get(f"{labs_api_url}/resources/resource/copilot-instructions.md", headers=headers)
    if response.status_code != 200:
        return f"Error fetching instructions from API: {response.status_code}"

    copilot_instructions = response.json()
    return copilot_instructions["resource"]



def main() -> None:
    """Runs the MCP server"""
    print("Starting MCP server")
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
