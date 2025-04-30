from mcp.server.fastmcp import FastMCP
import requests

mcp = FastMCP("mcp-server-for-foundry-catalog")

GH_GUIDANCE = """
# Model Integration Instructions (Agent Use Only)

This guide outlines how an agent can access and interact with a hosted Azure inference model using the `azure-ai-inference` SDK in Python. Authentication is handled via the `GITHUB_TOKEN` environment variable, and all requests are routed through the Azure GitHub-hosted endpoint.

## Requirements

- **Python** `>= 3.8`
- **Environment Variable:** `GITHUB_TOKEN` must be set with a valid GitHub Personal Access Token (PAT) with `models:read` scope.

## Installation

```bash
pip install azure-ai-inference
```

## Client Initialization

```python
import os
from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential

endpoint = "https://models.github.ai/inference"
token = os.environ["GITHUB_TOKEN"]

client = ChatCompletionsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(token),
)
```

## Usage Patterns

### Single-Turn Chat Completion

```python
from azure.ai.inference.models import UserMessage

response = client.complete(
    messages=[
        UserMessage("What is the capital of France?"),
    ],
    model={{inference_model_name}}  # Provided to the agent
)

content = response.choices[0].message.content
```

### Multi-Turn Conversation

Maintain message history manually across turns.

```python
from azure.ai.inference.models import UserMessage, AssistantMessage

messages = [
    UserMessage("Who was the first president of the U.S.?"),
    AssistantMessage("George Washington."),
    UserMessage("And the second?"),
]

response = client.complete(messages=messages, model={{inference_model_name}})
content = response.choices[0].message.content
```

### Streaming Output (Partial Token Delivery)

```python
from azure.ai.inference.models import UserMessage

response = client.complete(
    stream=True,
    messages=[
        UserMessage("List 3 benefits of daily meditation."),
    ],
    model_extras={'stream_options': {'include_usage': True}},
    model={{inference_model_name}}
)

final_usage = {}
for update in response:
    if update.choices and update.choices[0].delta:
        print(update.choices[0].delta.content or "", end="")
    if update.usage:
        final_usage = update.usage
```

## Scaling Beyond Free Limits

This integration uses GitHub token-based access via the `models.github.ai/inference` endpoint. For production or high-throughput scenarios, provision the model through an Azure subscription and authenticate with Azure credentials. No SDK code changes are required beyond swapping the credential type.

---

> ⚠️ This file is for internal agent integration only. It assumes secure handling of credentials and dynamic assignment of `inference_model_name` during runtime.

"""


@mcp.tool()
async def get_github_models_list() -> str:
    """Get a list of all supported projects from Azure AI Foundry."""
    url = "https://api.catalog.azureml.ms/asset-gallery/v1.0/models"
    body =  {
        "filters": [
            {"field": "azureOffers", "values": ["standard-paygo"], "operator": "eq"},
            {"field": "freePlayground", "values": ["true"], "operator": "eq"},
            {"field": "labels", "values": ["latest"], "operator": "eq"}
        ]
    }
    response = requests.post(url, json=body)

    resJson = response.json()

    text_models = []

    for summary in resJson["summaries"]:
        if "text" in summary["modelLimits"]["supportedOutputModalities"] and "text" in summary["modelLimits"]["supportedInputModalities"]:
            text_model = {
                "name": summary["name"],
                "inference_model_name": summary["publisher"].replace(" ", "-") + "/" + summary["name"],
                "summary": summary["summary"]
            }
            text_models.append(text_model)

    return text_models

@mcp.tool()
async def get_implementation_details_for_github_model(inference_model_name: str) -> str:
    """
    Detailed usage guidance (scripts, docs, etc) on how to implement a particular project from GitHub Models.
    Use this tool to get the implementation details of a project.
    Do not assume you know how to implement a project just because you know the project name.

    Args:
        project_name: name of project
    """


    guidance = GH_GUIDANCE.replace("{{inference_model_name}}", inference_model_name)

    return guidance

if __name__ == "__main__":
    mcp.run(transport="stdio")
