#!/usr/bin/env python3
"""Entrypoint for nanobot gateway in Docker."""
import json
import os
import sys

def main():
    config_path = "/app/nanobot/config.json"
    resolved_path = "/app/nanobot/config.resolved.json"
    workspace = os.environ.get("NANOBOT_WORKSPACE", "/app/nanobot/workspace")
    
    with open(config_path, "r") as f:
        config = json.load(f)
    
    # LLM config
    if os.environ.get("LLM_API_KEY"):
        config["providers"]["custom"]["apiKey"] = os.environ["LLM_API_KEY"]
    if os.environ.get("LLM_API_BASE_URL"):
        config["providers"]["custom"]["apiBase"] = os.environ["LLM_API_BASE_URL"]
    if os.environ.get("LLM_API_MODEL"):
        config["agents"]["defaults"]["model"] = os.environ["LLM_API_MODEL"]
    
    # Gateway
    config["gateway"] = {
        "host": os.environ.get("NANOBOT_GATEWAY_CONTAINER_ADDRESS", "0.0.0.0"),
        "port": int(os.environ.get("NANOBOT_GATEWAY_CONTAINER_PORT", "8080"))
    }
    
    # LMS MCP
    config["tools"]["mcpServers"]["lms"] = {
        "command": "python",
        "args": ["-m", "mcp_lms", os.environ.get("NANOBOT_LMS_BACKEND_URL", "http://backend:8000")],
        "env": {
            "NANOBOT_LMS_BACKEND_URL": os.environ.get("NANOBOT_LMS_BACKEND_URL", "http://backend:8000"),
            "LMS_BACKEND_URL": os.environ.get("LMS_BACKEND_URL", "http://backend:8000"),
            "LMS_API_KEY": os.environ.get("LMS_API_KEY", "")
        }
    }
    
    # Webchat channel
    config["channels"] = {
        "webchat": {
            "enabled": True,
            "host": os.environ.get("NANOBOT_WEBCHAT_CONTAINER_ADDRESS", "0.0.0.0"),
            "port": int(os.environ.get("NANOBOT_WEBCHAT_CONTAINER_PORT", "8080")),
            "allowFrom": ["*"]
        }
    }
    
    # Observability MCP server
    config["tools"]["mcpServers"]["obs"] = {
        "command": "python",
        "args": ["-m", "mcp_obs"],
        "env": {
            "VICTORIALOGS_URL": "http://victorialogs:9428",
            "VICTORIATRACES_URL": "http://victoriatraces:10428"
        }
    }

    # Webchat MCP for UI messages
    config["tools"]["mcpServers"]["webchat"] = {
        "command": "python",
        "args": ["-m", "mcp_webchat"],
        "env": {
            "NANOBOT_WEBCHAT_RELAY_URL": os.environ.get("NANOBOT_WEBCHAT_RELAY_URL", "http://nanobot:8080"),
            "NANOBOT_WEBCHAT_RELAY_TOKEN": os.environ.get("NANOBOT_ACCESS_KEY", "webchat-token")
        }
    }
    
    with open(resolved_path, "w") as f:
        json.dump(config, f, indent=2)
    
    print(f"Using config: {resolved_path}", file=sys.stderr)
    os.execvp("uv", ["uv", "run", "nanobot", "gateway", "--config", resolved_path, "--workspace", workspace])

if __name__ == "__main__":
    main()
