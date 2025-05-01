# 🧠 MCP Server for Azure AI Foundry Catalog

Explore and use models from **Azure AI Foundry Catalog** (currently supports GitHub Models).

---

## 🛠 Tools Provided

- `get_github_models_list`: Lists available models from the Foundry Catalog.
- `get_implementation_details_for_github_model`: Retrieves implementation guidance for a specific Foundry model.

---

<a href="https://github.com/tendau/foundrylabsagent/generate" target="_blank">
  <img src="https://img.shields.io/badge/-Use%20this%20template-2ea44f?style=for-the-badge&logo=github" alt="Use The Template">
</a>

> 🛠️ **This will fork a template repo with minimal setup for MCP Servers so you can quickly build your own prototypes.**
>
> Included MCP Servers:
> - MCP Server for Azure AI Foundry Catalog (this server)
> - [MCP Server for Azure AI Foundry Labs](./azure-ai-foundry-labs-mcp-server.md)

---

## 🚀 Getting Started

### ✅ Recommended (Codespaces)

1. Click the **"Use this template"** button above to create your own copy of the project.
2. Open your new repo in **GitHub Codespaces** — the servers will start automatically via the dev container.
3. GitHub Codespaces will show you README.md. Follow instructions there to get started!

---

### 🧑‍🔧 Manual Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/tendau/foundrylabsagent
   cd foundrylabsagent
   ```

2. Add the following entry to your MCP client (e.g., Copilot Labs) configuration:

   ```json
   {
     "Foundry Catalog MCP": {
       "command": "uv",
       "args": [
         "--directory",
         "C:/Users/your-username/path/to/mcp-foundry/src/python",
         "run",
         "-m",
         "mcp_server_for_foundry_catalog"
       ]
     }
   }
   ```

   > Adjust the path above to reflect your local environment.

---

## 💡 Notes

- This is a **stdio-based MCP server**.
- It will be auto-invoked by GitHub Copilot when configured correctly.
