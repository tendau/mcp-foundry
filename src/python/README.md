# azure-agent-mcp-server
The python project  for the MCP servers, powered by uv.

## Publishing
To build and publish this package, we use uv and publish to our team's Azure Artifacts Feed.

1. Set up Azure Artifacts feed credentials through env variables. On powershell, set `$env:UV_INDEX_TNRDEV_USERNAME="dummy"` and `$env:UV_INDEX_TNRDEV_PASSWORD=<personal_access_token>`.
2. Update the version number in pyproject.toml to your new desired version.
3. Build the distribution: `uv build`. You should see the correctly versioned distribution appear in a `dist/` folder.
4. Publish: `uv publish --index tnrdev`


## Running the MCP server using uvx
The easiest way to run one of the  MCP servers is through uvx, which will do a cached install of the package.
For example, to run the `mcp-server-for-foundry-labs`, run the following command:
```bash
uvx --index-url "https://dummy:<personal-access-token>@pkgs.dev.azure.com/tnrdev/_packaging/tnrdev/pypi/simple/" --from azure-agent-mcp-server mcp-server-for-foundry-labs
```
