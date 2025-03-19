# Azure AI Agent Service MCP Server

Python module for a Model Context Protocol (MCP) server that enables Claude Desktop to search content using Azure AI services.

## Features

- **Azure AI Search Tool** - Search your indexed documents with AI-enhanced results
- **Bing Web Grounding Tool** - Search the web with source citations
- **Intelligent Processing** - Azure AI Agent Service optimizes search results with intelligent processing
- **Multiple Data Sources** - Search both private documents and the public web
- **Source Citations** - Web search results include citations to original sources

## Installation

### Prerequisites
- Python 3.10+
- Azure AI Project with configured connections
- Azure AI Search service with indexed content

### Setup

1. **Install the package:**
   ```bash
   # Create and activate virtual environment
   uv venv
   .venv\Scripts\activate  # On Windows
   source .venv/bin/activate  # On macOS/Linux

   # Install dependencies
   uv add mcp[cli] azure-identity python-dotenv azure-ai-projects
   ```

2. **Configure environment variables:**
   Create an `.env` file with:
   ```bash
   PROJECT_CONNECTION_STRING=your-project-connection-string
   MODEL_DEPLOYMENT_NAME=your-model-deployment-name
   AI_SEARCH_CONNECTION_NAME=your-search-connection-name
   BING_CONNECTION_NAME=your-bing-connection-name
   AI_SEARCH_INDEX_NAME=your-index-name
   ```

## Usage

### Running the Server

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

## API Reference

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