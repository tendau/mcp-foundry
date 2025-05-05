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
>
> Included MCP Servers:
>
> - MCP Server for Azure AI Foundry Labs (this server)
> - [MCP Server for Azure AI Foundry Catalog](./azure-ai-foundry-catalog-mcp-server.md)

---

## 🚀 Getting Started

### ✅ Recommended (Codespaces)

1. Click the **"Use this template"** button above to create your own copy of the project.
2. Open your new repo in **GitHub Codespaces** — the servers will start automatically via the dev container.
3. GitHub Codespaces will show you README.md. Follow instructions there to get started!

---

## 🧑‍🔧 Manual Setup

### 1. Install Python and pipx

Make sure you have **Python** installed along with **pipx**.  
Most modern Python installations include `pipx`, but if you don’t have it, you can install it with:

```bash
python -m pip install --user pipx
python -m pipx ensurepath
```

---

### 2. Configure Your MCP Client

Open the **MCP settings** in your client of choice.  
Follow the appropriate link below for detailed instructions:

- [Visual Studio Code – Copilot Chat](https://code.visualstudio.com/docs/copilot/chat/mcp-servers)
- [Claude](https://modelcontextprotocol.io/quickstart/user)
- [Cursor](https://docs.cursor.com/context/model-context-protocol)

---

### 3. Add Foundry Labs MCP Entry

Copy and paste the following JSON block into your MCP client’s configuration:

```json
"MCP Server For Foundry Labs": {
  "command": "pipx",
  "args": [
    "run",
    "--spec",
    "git+https://github.com/tendau/mcp-foundry.git@topic/folderstruct#subdirectory=src/python",
    "azure-ai-foundry-labs-mcp-server"
  ]
}
```

> This will automatically install and run the MCP server for Foundry Labs using `pipx`.

---

You're now ready to use Foundry Labs with your preferred MCP-enabled client!

## 💡 Notes

- This is a **stdio-based MCP server**.
- GitHub Copilot invokes it automatically once it detects tool availability.
