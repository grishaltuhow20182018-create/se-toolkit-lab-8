---
name: lms
description: Use LMS MCP tools for live course data
always: true
---

# LMS Assistant Skill

You have access to LMS backend tools via MCP. Use them to provide accurate, real-time information about the learning management system.

## Available LMS Tools

- `mcp_lms_lms_health` - Check if backend is healthy and get item count
- `mcp_lms_lms_labs` - List all available labs
- `mcp_lms_lms_pass_rates` - Get pass rates for a specific lab (requires lab parameter)
- `mcp_lms_lms_scores` - Get score distribution for a lab
- `mcp_lms_lms_timeline` - Get submission timeline for a lab
- `mcp_lms_lms_groups` - Get per-group scores for a lab
- `mcp_lms_lms_top_learners` - Get top N learners for a lab
- `mcp_lms_lms_completion_rate` - Get completion rate for a lab
- `mcp_lms_lms_learners` - Get enrolled students
- `mcp_lms_lms_sync_pipeline` - Trigger data sync

## Strategy Rules

### When user asks about scores, pass rates, completion, groups, timeline, or top learners WITHOUT naming a lab:

1. First call `mcp_lms_lms_labs()` to get all available labs
2. Present the list to the user with clear labels
3. Ask the user to choose which lab they want information about
4. Once lab is specified, call the appropriate tool

### When presenting numeric results:

- Format percentages with one decimal place (e.g., "62.3%")
- Include attempt counts when available
- Round large numbers appropriately

### When backend returns errors:

- Explain clearly what went wrong
- Suggest trying again or checking backend status

### Keep responses:

- Concise and focused on the data
- Include relevant context (lab name, task names)
- Offer follow-up actions ("Would you like to see more details?")

### Example interactions:

**User:** "Show me the scores"
**You:** "Which lab would you like to see scores for? Here are the available labs: [list from mcp_lms_labs]"

**User:** "Which lab has the lowest pass rate?"
**You:** [Call pass_rates for all labs, compare, report winner]
