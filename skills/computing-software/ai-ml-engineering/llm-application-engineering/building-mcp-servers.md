---
id: computing-software.ai-ml-engineering.llm-application-engineering.building-mcp-servers
name: building-mcp-servers
category: computing-software
field: ai-ml-engineering
product: llm-application-engineering
tags: [llm-application, tool-use, mcp, model-context-protocol, fastmcp, mcp-connector, streamable-http]
level: practitioner
status: docs-checked
description: "Build and connect Model Context Protocol servers: Python SDK tools/resources, stdio vs Streamable HTTP, auth, MCP Inspector testing, Claude API MCP connector."
sources:
  - https://modelcontextprotocol.io/docs/develop/build-server
  - https://modelcontextprotocol.io/specification/2025-11-25/basic/transports
  - https://modelcontextprotocol.io/specification/latest/basic/authorization
  - https://modelcontextprotocol.io/docs/tools/inspector
  - https://github.com/modelcontextprotocol/python-sdk
  - https://platform.claude.com/docs/en/agents-and-tools/mcp-connector
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Model Context Protocol servers

MCP standardises how LLM apps (desktop assistants, IDEs, agent frameworks, the Claude API) discover and call external tools, read resources and use prompt templates. One server, many clients.

## Minimal server (Python SDK)
```python
# pip install "mcp[cli]"   (or: uv add "mcp[cli]"; Python 3.11+)
from mcp.server import MCPServer
mcp = MCPServer("tickets")

@mcp.tool()
def search_tickets(query: str, status: str = "open", limit: int = 10) -> list[dict]:
    """Search support tickets by text. status: open|closed|all. Returns id, title, status, updated_at."""
    return db.search(query, status, min(limit, 50))

@mcp.resource("ticket://{ticket_id}")
def ticket(ticket_id: str) -> str:
    """Full ticket thread as text."""
    return db.thread(ticket_id)

if __name__ == "__main__":
    mcp.run(transport="stdio")
```
The current official Python SDK (v2 docs) uses `MCPServer` from `mcp.server`; older SDK versions used `FastMCP` from `mcp.server.fastmcp`, so match the import to the installed version. Type hints and docstrings generate the tool schema and description - write them as carefully as any tool description. The SDK README states it can serve stdio, Streamable HTTP and SSE, and `uv run mcp run server.py --transport streamable-http` serves a server over HTTP (default URL path shown in the README: `http://localhost:8000/mcp`).

## Transports
- **stdio:** the client launches the server as a subprocess; local. The server MUST NOT write anything to stdout that is not a valid MCP message; it MAY write UTF-8 logs to stderr, which clients should not treat as errors. Use the standard `logging` module (stderr) instead of `print()`.
- **Streamable HTTP:** remote, multi-user servers; the spec says it replaces the older HTTP+SSE transport (2024-11-05), which is deprecated. Servers MUST validate the `Origin` header on all incoming connections (respond 403 for an invalid one) to prevent DNS rebinding, and SHOULD bind only to localhost (127.0.0.1) rather than 0.0.0.0 when running locally. Standard output logging is fine for HTTP servers.
- **Authorization:** the spec's authorization flow applies to HTTP-based transports (servers act as OAuth 2.1 resource servers and MUST implement OAuth 2.0 Protected Resource Metadata, RFC 9728). Stdio implementations SHOULD NOT follow it and instead retrieve credentials from the environment.

## Testing and connecting
- MCP Inspector (needs Node 22.19.0 or newer): `npx @modelcontextprotocol/inspector node path/to/server/index.js` for the web client, add `--cli` for a scriptable client (for example `--method tools/list`) or `--tui` for a terminal UI. The Python SDK also offers `uv run mcp dev server.py`, which opens the server in the Inspector.
- Claude API MCP connector (remote servers only): the server must be publicly exposed over HTTP (Streamable HTTP and SSE are supported); local stdio servers cannot be connected directly.
```python
client.beta.messages.create(
    model="claude-sonnet-5-5", max_tokens=4096, betas=["mcp-client-2025-11-20"],
    mcp_servers=[{"type": "url", "url": "https://mcp.example.com/mcp", "name": "tickets",
                  "authorization_token": TOKEN}],
    tools=[{"type": "mcp_toolset", "mcp_server_name": "tickets"}],
    messages=[...],
)
```
Both halves are required: the `mcp_servers` array (URL, authentication) plus a matching `mcp_toolset` entry in `tools`. The toolset supports allowlisting and denylisting individual tools; the docs recommend denylisting write or destructive tools for read-only assistants or when you want human confirmation before state changes.

## Security
- Tools run with the server's credentials: scope them per user, enforce authorization inside each tool, and keep destructive tools behind confirmation (practitioner advice).
- Treat tool descriptions and results from third-party servers as untrusted input (indirect prompt injection); pin server versions and review what you install (practitioner advice).
- Cap result sizes and paginate; huge results blow the client's context (practitioner advice).

## Verify
- [ ] Inspector lists tools with correct schemas; each tool called once successfully and once with bad input (clear error).
- [ ] stdio server emits nothing on stdout except protocol messages.

## Checked
Method: docs-checked 2026-11-09 against the MCP build-server guide (Python logging and Inspector passages), the 2025-11-25 transports and latest stdio, Streamable HTTP and authorization spec pages (read by keyword search), the Inspector page, the python-sdk README (read in the install and quickstart portions) and the Claude MCP connector page (by keyword search). Dropped: the `claude mcp add` command, the `@mcp.prompt()` example, and the specific "OAuth 2.1 per spec for remote servers" wording beyond what the authorization page states.
