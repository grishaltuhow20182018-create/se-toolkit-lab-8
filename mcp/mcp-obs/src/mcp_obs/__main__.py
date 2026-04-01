"""Entry point for running mcp_obs as an MCP server."""
from mcp_obs.server import mcp

if __name__ == "__main__":
    mcp.run()
