from mcp.server.fastmcp import FastMCP
import requests
import os
from dotenv import load_dotenv

load_dotenv()

mcp = FastMCP("azure-ai-foundry-models-mcp-server")
labs_api_url = os.environ.get("LABS_API_URL", "https://labs-mcp-api.azurewebsites.net//api/v1")


@mcp.tool()
async def get_foundry_models_list() -> str:
    """Get a list of all supported projects from Azure AI Foundry."""
    url = "https://api.catalog.azureml.ms/asset-gallery/v1.0/models"
    body = {
        "filters": [
            {"field": "azureOffers", "values": ["standard-paygo"], "operator": "eq"},
            {"field": "freePlayground", "values": ["true"], "operator": "eq"},
            {"field": "labels", "values": ["latest"], "operator": "eq"},
        ]
    }
    response = requests.post(url, json=body)

    resJson = response.json()

    text_models = []

    for summary in resJson["summaries"]:
        if (
            "text" in summary["modelLimits"]["supportedOutputModalities"]
            and "text" in summary["modelLimits"]["supportedInputModalities"]
        ):
            text_model = {
                "name": summary["name"],
                "inference_model_name": summary["publisher"].replace(" ", "-") + "/" + summary["name"],
                "summary": summary["summary"],
            }
            text_models.append(text_model)

    return text_models


@mcp.tool()
async def get_implementation_details_for_foundry_model(inference_model_name: str) -> str:
    """
    Detailed usage guidance (scripts, docs, etc) on how to implement a particular project from GitHub Models.
    Use this tool to get the implementation details of a project.
    Do not assume you know how to implement a project just because you know the project name.

    Args:
        project_name: name of project
    """

    response = requests.get(f"{labs_api_url}/resources/resource/gh_guidance.md")
    if response.status_code != 200:
        return f"Error fetching projects from API: {response.status_code}"

    guidance = response.json()
    GH_GUIDANCE = guidance["resource"]["content"]

    guidance = GH_GUIDANCE.replace("{{inference_model_name}}", inference_model_name)

    return guidance


@mcp.resource("foundry://copilot-instructions")
def get_foundry_copilot_instructions() -> str:
    """Get instructions for using Foundry Copilot."""

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
