---
name: observability
description: Use observability tools to debug issues and search logs/traces
always: true
---

# Observability Skill

You have access to observability tools for querying VictoriaLogs and VictoriaTraces.

## Available Tools

### Log Tools (VictoriaLogs)
- logs_search(query, limit) - Search logs by LogsQL query
- logs_error_count(service, minutes) - Count errors per service

### Trace Tools (VictoriaTraces)
- traces_list(service, limit) - List recent traces for a service
- traces_get(trace_id) - Fetch a specific trace by ID

### Cron Tools
- cron(action, ...) - Schedule recurring jobs

## When to Use

### User asks "What went wrong?" or "Check system health"
1. First call logs_error_count("Learning Management Service", 10)
2. If errors found, call logs_search("severity:ERROR", 10)
3. Extract trace_id from log results
4. Call traces_get(trace_id) to see full trace
5. Summarize findings concisely - mention BOTH log evidence AND trace evidence
6. Name the affected service and root failing operation

### User asks about errors
1. Call logs_error_count("Learning Management Service", 10)
2. If errors found, call logs_search("severity:ERROR", 10)
3. If you find a trace_id, call traces_get(trace_id)

## Response Guidelines

- Be concise - Dont dump raw JSON
- Summarize findings
- Highlight key info: service name, error type, trace_id
- For "What went wrong?" - cite at least one log AND one trace
- Mention the affected service and failing operation

## Example Investigation Flow

1. logs_error_count("Learning Management Service", 10) → finds 1 error
2. logs_search("severity:ERROR", 10) → finds log with trace_id=abc123
3. traces_get("abc123") → shows span hierarchy with DB failure
4. Summary: "The LMS backend failed due to PostgreSQL connection error. 
   Log shows 'connection refused' at 23:45:00. Trace abc123 shows the 
   db_query span failed after 5ms retry timeout."
