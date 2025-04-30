# 🧠 MCP Server for GitHub Models

This server exposes tools for Copilot to interact with models from the **Foundry Catalog**.

---

## 🛠 Tools Provided

- `get_foundry_models_list`: Lists available models from the Foundry Catalog.
- `get_implementation_details_for_foundry_model`: Retrieves implementation guidance for a specific Foundry model.

---

[![Use The Template](https://img.shields.io/badge/-Use%20this%20template-2ea44f?style=for-the-badge&logo=github)](https://github.com/tendau/foundrylabsagent/generate)

---

## 🚀 Getting Started

### ✅ Recommended (Codespaces)

1. Click the **"Use this template"** button above to create your own copy of the project.
2. Open your new repo in **GitHub Codespaces** — the servers will start automatically via the dev container.

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
