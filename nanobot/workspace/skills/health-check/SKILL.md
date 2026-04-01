---
name: health-check
description: Proactive health monitoring with scheduled reports
always: false
---

# Health Check Skill

## Purpose
Automatically monitor LMS backend health and post reports to the active chat.

## When to Run

### Scheduled (every 2 minutes)
1. Call `mcp_lms_lms_health()` to check backend status
2. Call `mcp_obs_logs_error_count("Learning Management Service", 2)` for recent errors
3. If errors found:
   - Call `mcp_obs_logs_search("severity:ERROR", 5)` for details
   - Extract trace_id if present
   - Call `mcp_obs_traces_get(trace_id)` for full trace
4. Post concise health report to chat

## Response Guidelines
- Keep reports under 150 words
- Use emoji indicators (✅ ⚠️ ❌)
- Include specific error messages and trace IDs
- Provide actionable recommendations
