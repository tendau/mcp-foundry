# Azure AI Agent Service MCP Server

This Model Context Protocol (MCP) server enables Claude Desktop to search your content using Azure AI services. It provides access to both document search capabilities via Azure AI Search and web search via Bing Web Grounding tools.

## Features

- **Azure AI Search Tool** - Search your indexed documents with AI-enhanced results
- **Bing Web Grounding Tool** - Search the web with source citations
- **Intelligent Processing** - Azure AI Agent Service optimizes search results with intelligent processing
- **Multiple Data Sources** - Search both private documents and the public web
- **Source Citations** - Web search results include citations to original sources

## Requirements

- **Python:** Version 3.10 or higher
- **Claude Desktop:** Latest version
- **Azure Resources:** 
  - Azure AI Project with Azure AI Search and Bing connections
  - Azure AI Search service with an index containing vectorized text data

## Setup

### 1. Azure AI Project Configuration

Before using the server, you need to:

1. **Create an Azure AI Project:**
   - Go to the Azure Portal and create a new Azure AI Project
   - Note the project connection string and model deployment name

2. **Create an Azure AI Search Connection:**
   - In your Azure AI Project, add a connection to your Azure AI Search service
   - Note the connection name and index name

3. **Create a Bing Web Search Connection:**
   - In your Azure AI Project, add a connection to Bing Search service
   - Note the connection name

4. **Authenticate with Azure:**
   ```bash
   az login
   ```

### 2. Environment Setup

Create an environment file (`.env`) with the following variables:

```bash
PROJECT_CONNECTION_STRING=your-project-connection-string
MODEL_DEPLOYMENT_NAME=your-model-deployment-name
AI_SEARCH_CONNECTION_NAME=your-search-connection-name
BING_CONNECTION_NAME=your-bing-connection-name
AI_SEARCH_INDEX_NAME=your-index-name
```

### 3. Python Environment

```bash
# Create and activate virtual environment
uv venv
.venv\Scripts\activate  # On Windows
source .venv/bin/activate  # On macOS/Linux

# Install dependencies
uv add mcp[cli] azure-identity python-dotenv azure-ai-projects
```

## Usage

### Running the Server Directly

```bash
python -m mcp_server_azure_ai_agent
```

### Claude Desktop Configuration

Add the following to your Claude Desktop configuration file:

```json
{
  "mcpServers": {
    "azure-ai-agent": {
      "command": "uv",
      "args": [
        "--directory",
        "/ABSOLUTE/PATH/TO/PARENT/FOLDER",
        "run",
        "-m", "mcp_server_azure_ai_agent"
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

## Testing Your Server

Once configured in Claude Desktop, you can try commands like:

- "Search my documents for information about machine learning"
- "Find current news about artificial intelligence on the web"

## Available Tools

### 1. `search_index`

Search your Azure AI Search index using the optimal retrieval method.

**Parameters:**
- `query` (string): The search query text
- `top` (integer, optional): Maximum number of results to return (default: 5)

**Example:**
````

### 2. `web_search`

Search the web using Bing Web Grounding to find the most current information.

**Parameters:**
- `query` (string): The search query text

**Example:**
```
Search the web for the latest developments in large language models
```

## Troubleshooting

- **Connection Issues:**
  - Verify your Azure credentials are valid
  - Check your connection strings and names
  - Ensure your Azure AI Project has the correct connections configured

- **Search Failures:**
  - Verify your index exists and contains data
  - Check that your search query is valid
  - Review the server logs for detailed error messages

## License

This project is licensed under the MIT License.