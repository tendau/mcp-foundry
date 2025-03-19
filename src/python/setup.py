from setuptools import setup, find_packages

setup(
    name="mcp-server-azure-ai-agent",
    version="0.1.0",
    description="Azure AI Agent Service MCP Server",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Farzad Sunavala",
    author_email="fsunavala@microsoft.com",
    url="https://github.com/modelcontextprotocol/servers",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.10",
    install_requires=[
        "mcp[cli]",
        "azure-identity",
        "python-dotenv",
        "azure-ai-projects"
    ],
    entry_points={
        "console_scripts": [
            "mcp-server-azure-ai-agent=mcp_server_azure_ai_agent.__main__:main",
        ],
    },
)