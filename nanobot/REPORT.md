
# Lab 8 Report

## Task 1A — Bare agent

### Q1: "Hello! What can you do?"

**Response:**
Hello! I'm nanobot 🐈, your personal AI assistant. I can help you with a wide variety of tasks:

Core Capabilities:
- File operations (read, write, edit, list directories)
- Shell command execution (with safety limits)
- Web search and content fetching
- Scheduling reminders and recurring tasks
- Sending messages with file attachments

Special Skills:
- structured-ui: Interactive choice interfaces for selections
- memory: Two-layer memory system (long-term facts + searchable history)
- weather: Current weather and forecasts (no API key needed)
- cron: Schedule reminders and recurring tasks
- tmux: Remote-control tmux sessions
- skill-creator: Create or update custom AgentSkills

### Q2: "What is the agentic loop?"

**Response:**
The agentic loop is the fundamental cycle that autonomous AI agents follow to interact with their environment:

1. Perceive - Observe the current state of the environment (sensors, inputs, context)
2. Reason - Process information, plan, and decide what to do next (thinking, planning, tool selection)
3. Act - Execute an action (call tools, send messages, modify files, etc.)
4. Repeat - Go back to step 1 with updated state

This loop continues until a goal is achieved or a stopping condition is met.

### Q3: "What labs are available in our LMS?"

**Response:**
The agent does NOT have access to real LMS backend data yet. It only sees local workspace folders:
- memory
- sessions  
- skills

This is expected — MCP tools are not configured yet.

---

## Task 1B — Agent with LMS tools

### Q1: "What labs are available in our LMS?"

**Response:**
Here are the labs available in our LMS:

1. Lab 01 – Products, Architecture & Roles
2. Lab 02 — Run, Fix, and Deploy a Backend Service
3. Lab 03 — Backend API: Explore, Debug, Implement, Deploy
4. Lab 04 — Testing, Front-end, and AI Agents
5. Lab 05 — Data Pipeline and Analytics Dashboard
6. Lab 06 — Build Your Own Agent
7. Lab 07 — Build a Client with an AI Coding Agent
8. lab-08 (title not specified)

**MCP Tools Registered:**
- mcp_lms_lms_health
- mcp_lms_lms_labs
- mcp_lms_lms_learners
- mcp_lms_lms_pass_rates
- mcp_lms_lms_timeline
- mcp_lms_lms_groups
- mcp_lms_lms_top_learners
- mcp_lms_lms_completion_rate
- mcp_lms_lms_sync_pipeline

### Q2: "Is the LMS backend healthy?"

**Response:**
The LMS backend is healthy. There are currently 56 items.

**Tools used:** `mcp_lms_lms_health`

---

### Q3: "Which lab has the lowest pass rate?"

**Response:**
Lab 05 – Data Pipeline and Analytics Dashboard, with an average score of 20.0 for the main task "Optional: Plan skill development". This is significantly lower than other labs' main task scores, which range from 36.4 (Lab 07) to 84.3 (Lab 01).

**Tools used:** 
- `mcp_lms_lms_labs` - to get all labs
- `mcp_lms_lms_pass_rates` - called for each lab to compare

**Agent behavior:**
- Agent called lms_labs() first to get the list of labs
- Then called lms_pass_rates() for each lab individually
- Compared the results and identified Lab 05 as having the lowest pass rate
- Provided detailed explanation with specific numbers

---

## Task 1C — Skill prompt

Отлично! Агент спросил, какой лаб выбрать! 🎉

Это именно то, что должен делать skill prompt! Но я заметил, что агент не показал список лабов — просто спросил идентификатор. Давай проверим, загрузился ли skill:

# Проверь, что skill файл существует
cat workspace/skills/lms/SKILL.md | head -20
Возможно, skill не загрузился автоматически. Давай обновим конфиг, чтобы skill точно применялся:

nano ~/.nanobot/config.json
Добавь skills секцию:

{
  "agents": {
    "defaults": {
      "workspace": "/root/se-toolkit-lab-8/nanobot/workspace",
      "model": "openrouter/free",
      "provider": "custom",
      "skills": ["lms"]
    }
  },
  "providers": {
    "custom": {
      "apiKey": "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",
      "apiBase": "https://openrouter.ai/api/v1"
    }
  },
  "tools": {
    "mcpServers": {
      "lms": {
        "command": "python",
        "args": ["-m", "mcp_lms"],
        "env": {
          "NANOBOT_LMS_BACKEND_URL": "http://localhost:42002",
          "NANOBOT_LMS_API_KEY": "set-it-to-something-and-remember-it"
        }
      }
    }
  }
}
Или skill может загружаться автоматически из workspace/skills/. Проверь структуру:

ls -la workspace/skills/
ls -la workspace/skills/lms/
Для REPORT.md запиши этот результат:

## Task 1C — Skill prompt

### Test: "Show me the scores" (without specifying a lab)

**Response:**
"I need to know which specific lab you're interested in. Could you please provide the lab identifier (e.g., 'lab-04')?"

**Expected behavior:**
- Agent should ask for lab selection when lab parameter is missing
- Ideally, agent should first call lms_labs() and present choices
- Current behavior: Agent asks for lab identifier directly (acceptable)

**Skill file created:** `workspace/skills/lms/SKILL.md`

**Skill teaches:**
- When to call lms_labs() first (when lab not specified)
- How to present lab choices to user
- How to format numeric results (percentages, counts)
- When to trigger sync pipeline
## Task 2A — Deployed agent

### Startup Log Excerpt

nanobot-1 | Building lms-backend @ file:///app/backend
nanobot-1 | Building mcp-lms @ file:///app/mcp/mcp-lms
nanobot-1 | Building qwen-code-api @ file:///app/qwen-code-api
nanobot-1 | Built qwen-code-api
nanobot-1 | Built mcp-lms
nanobot-1 | Built lms-backend
nanobot-1 | Using config: /app/nanobot/config.resolved.json
nanobot-1 | LMS Backend URL: http://backend:8000
nanobot-1 | Starting nanobot gateway version 0.1.4.post5 on port 8080…
nanobot-1 | MCP: registered tool ‘mcp_lms_lms_health’ from server ‘lms’
nanobot-1 | MCP: registered tool ‘mcp_lms_lms_labs’ from server ‘lms’
nanobot-1 | MCP: registered tool ‘mcp_lms_lms_pass_rates’ from server ‘lms’
nanobot-1 | MCP server ‘lms’: connected, 9 tools registered
nanobot-1 | Agent loop started


### Status

- Nanobot gateway running as Docker service
- MCP LMS server connected (9 tools)
- Backend accessible at http://backend:8000

## Task 2B — Web client

### Completed
- Webchat channel plugin installed (`nanobot-webchat`, `mcp-webchat`)
- Caddyfile configured with `/flutter` and `/ws/chat` routes
- Nanobot gateway running with webchat channel support

### Issue
Flutter client build failed due to Docker registry authentication:
- `cirruslabs/flutter:3.41.2` image requires authentication
- Docker volume `client-web-flutter` is empty

### Workaround
The nanobot gateway is running and the WebSocket endpoint `/ws/chat` is configured.
The LMS Dashboard at http://<vm-ip>:42002/ shows all 56 items from the backend.

### Files Created/Modified
- `nanobot/Dockerfile` - Docker build for nanobot gateway
- `nanobot/entrypoint.py` - Runtime config injection
- `docker-compose.override.yml` - Service definitions
- `caddy/Caddyfile` - Added /flutter and /ws/chat routes
- `nanobot-websocket-channel/` - Git submodule for webchat

### Verification Commands
```bash
# Check nanobot is running
docker compose --env-file .env.docker.secret ps nanobot

# Check MCP tools registered
docker compose --env-file .env.docker.secret logs nanobot | grep "MCP server"

# Test WebSocket (if websocat available)
echo '{"content":"Hello"}' | websocat "ws://<vm-ip>:42002/ws/chat?access_key=YOUR_KEY"
