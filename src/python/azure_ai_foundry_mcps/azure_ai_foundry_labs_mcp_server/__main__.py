from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
import requests
import os

load_dotenv()

mcp = FastMCP("azure-ai-foundry-labs-mcp-server")
labs_api_url = os.environ.get("LABS_API_URL", "https://labs-mcp-api.azurewebsites.net//api/v1")


@mcp.tool()
async def get_azure_ai_foundry_labs_projects_list() -> str:
    """Get a list of all supported projects from Azure AI Foundry Labs."""

    response = requests.get(f"{labs_api_url}/projects?source=afl")
    if response.status_code != 200:
        return f"Error fetching projects from API: {response.status_code}"

    project_reponse = response.json()

    return project_reponse["projects"]


@mcp.tool()
async def get_implementation_details_for_labs_project(project_name: str) -> str:
    """
    Detailed usage guidance (scripts, docs, etc) on how to implement a particular project from GitHub Models.
    Use this tool to get the implementation details of a project.
    Do not assume you know how to implement a project just because you know the project name.

    Args:
        project_name: name of project
    """

    response = requests.get(f"{labs_api_url}/projects/{project_name}/implementation")
    if response.status_code != 200:
        return f"Error fetching projects from API: {response.status_code}"

    project_response = response.json()

    return project_response


@mcp.tool()
def get_foundry_copilot_instructions() -> str:
    """Get instructions for using Foundry Copilot.
    Only call this when someone asks for help using Foundry models or Foundry Labs."""

    response = requests.get(f"{labs_api_url}/resources/resource/copilot-instructions.md")
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
