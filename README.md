# Azure AI Agent Service MCP Server

A Model Context Protocol (MCP) server that enables Claude Desktop to search content using Azure AI Foundry - both document search via Azure AI Search and web search via Bing Web Grounding tools.

![demo](img/mcp-foundry-2.gif)



## Features

- 🔍 **Document Search** - Search indexed documents with Azure AI Search
- 🌐 **Web Search** - Find information online with Bing Web Grounding
- 💡 **Intelligent Results** - AI-optimized search results with source citations
- 🔗 **Multiple Sources** - Search across private documents and public web

## Prerequisites

- Python 3.10+
- Claude Desktop (latest version)
- Azure AI Project with Azure AI Search and Bing connections
- Azure AI Search service with an indexed collection

## Quick Start

### 1. Configure Azure

1. Create an Azure AI Project and note the connection string and model deployment name
2. Add an Azure AI Search connection and note connection name and index name
3. Add a Bing Web Search connection and note the connection name
4. Authenticate: `az login`

### 2. Set Environment Variables

Create an `.env` file:

```bash
PROJECT_CONNECTION_STRING=your-project-connection-string
MODEL_DEPLOYMENT_NAME=your-model-deployment-name
AI_SEARCH_CONNECTION_NAME=your-search-connection-name
BING_CONNECTION_NAME=your-bing-connection-name
AI_SEARCH_INDEX_NAME=your-index-name
```

### 3. Install and Run

```bash
# Setup environment
uv venv
.venv\Scripts\activate  # On Windows
source .venv/bin/activate  # On macOS/Linux

# Install dependencies
uv add mcp[cli] azure-identity python-dotenv azure-ai-projects

# Run server
python -m mcp_server_azure_ai_agent
```

### 4. Configure Claude Desktop

Add to your Claude Desktop configuration file:

```json
{
  "mcpServers": {
    "azure-ai-agent": {
      "command": "uv",
      "args": [
        "--directory",
        "/ABSOLUTE/PATH/TO/PARENT/FOLDER",
        "run",
        "-m",
        "mcp_server_azure_ai_agent"
      ],
      "env": {
        "PROJECT_CONNECTION_STRING": "your-project-connection-string",
        "MODEL_DEPLOYMENT_NAME": "your-model-deployment-name",
        "AI_SEARCH_CONNECTION_NAME": "your-search-connection-name",
        "BING_CONNECTION_NAME": "your-bing-connection-name",
        "AI_SEARCH_INDEX_NAME": "your-index-name"
      }
    }
  }
}
```

## Available Tools

### `search_index`

Search documents in your Azure AI Search index.

### `web_search`

Search the web using Bing Web Grounding.

## Troubleshooting

- **Connection Issues:** Verify Azure credentials, connection strings, and project configuration
- **Search Failures:** Ensure index exists, contains data, and queries are valid

## License

MIT License
