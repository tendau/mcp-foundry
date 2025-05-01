# 🧪 MCP Server for Azure AI Foundry Labs

Prototype with state-of-the-art projects led by Microsoft Research from **Azure AI Foundry Labs**.

---

## 🛠 Tools Provided

- `get_azure_ai_foundry_labs_projects_list`: Lists available projects from Foundry Labs.
- `get_implementation_details_for_labs_project`: Retrieves implementation guidance for a specific Labs project.

---

<a href="https://github.com/tendau/foundrylabsagent/generate" target="_blank">
  <img src="https://img.shields.io/badge/-Use%20this%20template-2ea44f?style=for-the-badge&logo=github" alt="Use The Template">
</a>

> 🛠️ **This will fork a template repo with minimal setup for MCP Servers so you can quickly build your own prototypes.**


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
     "Foundry Labs MCP": {
       "command": "uv",
       "args": [
         "--directory",
         "C:/Users/your-username/path/to/mcp-foundry/src/python",
         "run",
         "-m",
         "mcp_server_for_foundry_labs"
       ]
     }
   }
   ```

   > Adjust the path above to reflect your local environment.

---

## 💡 Notes

- This is a **stdio-based MCP server**.
- GitHub Copilot invokes it automatically once it detects tool availability.
