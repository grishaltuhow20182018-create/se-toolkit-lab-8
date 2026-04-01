"""MCP server for observability tools (VictoriaLogs and VictoriaTraces)."""
import asyncio
import httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("observability")

VICTORIALOGS_URL = "http://victorialogs:9428"
VICTORIATRACES_URL = "http://victoriatraces:10428"


@mcp.tool()
async def logs_search(query: str = "severity:ERROR", limit: int = 10) -> list[dict]:
    """Search VictoriaLogs by LogsQL query.
    
    Args:
        query: LogsQL query (e.g., 'severity:ERROR', 'service.name:"Learning Management Service"')
        limit: Maximum number of results
    
    Returns:
        List of log entries
    """
    async with httpx.AsyncClient() as client:
        url = f"{VICTORIALOGS_URL}/select/logsql/query"
        params = {"query": query, "limit": limit}
        try:
            resp = await client.get(url, params=params, timeout=10)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            return [{"error": str(e)}]


@mcp.tool()
async def logs_error_count(service: str = "Learning Management Service", minutes: int = 60) -> dict:
    """Count errors per service over a time window.
    
    Args:
        service: Service name to filter
        minutes: Time window in minutes
    
    Returns:
        Error count dictionary
    """
    query = f'_time:{minutes}m service.name:"{service}" severity:ERROR'
    results = await logs_search(query, limit=1000)
    return {"service": service, "error_count": len(results), "time_window_minutes": minutes, "logs": results[:10]}


@mcp.tool()
async def traces_list(service: str = "Learning Management Service", limit: int = 10) -> list[dict]:
    """List recent traces for a service.
    
    Args:
        service: Service name
        limit: Maximum number of traces
    
    Returns:
        List of trace summaries
    """
    async with httpx.AsyncClient() as client:
        url = f"{VICTORIATRACES_URL}/select/jaeger/api/traces"
        params = {"service": service, "limit": limit}
        try:
            resp = await client.get(url, params=params, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            return data.get("data", [])
        except Exception as e:
            return [{"error": str(e)}]


@mcp.tool()
async def traces_get(trace_id: str) -> dict:
    """Fetch a specific trace by ID.
    
    Args:
        trace_id: Trace ID to fetch
    
    Returns:
        Full trace data with spans
    """
    async with httpx.AsyncClient() as client:
        url = f"{VICTORIATRACES_URL}/select/jaeger/api/traces/{trace_id}"
        try:
            resp = await client.get(url, timeout=10)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            return {"error": str(e)}
