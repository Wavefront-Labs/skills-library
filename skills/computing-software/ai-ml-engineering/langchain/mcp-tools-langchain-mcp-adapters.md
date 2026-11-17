---
id: computing-software.ai-ml-engineering.langchain.mcp-tools-langchain-mcp-adapters
name: mcp-tools-langchain-mcp-adapters
category: computing-software
field: ai-ml-engineering
product: langchain
tags: [langchain, langchain-mcp-adapters, mcp, model-context-protocol, multiserverclient, mcpadapter, agent-tools]
level: practitioner
status: docs-checked
description: "Load MCP server tools into LangChain agents: legacy MultiServerMCPClient (now unmaintained) vs the newer langchain.mcp MCPAdapter, transports, sessions, headers, tool errors."
sources:
  - https://github.com/langchain-ai/langchain-mcp-adapters
  - https://docs.langchain.com/oss/python/langchain/mcp
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# MCP tools in LangChain agents

**Goal:** reuse tools exposed by MCP servers in a LangChain agent without writing wrappers.

## Which library
- The `langchain-mcp-adapters` repo README now states it is no longer actively maintained; MCP support moved into LangChain under the `langchain.mcp` namespace (`pip install "langchain[mcp]"`).
- Per the LangChain docs, `langchain.mcp` needs `langchain[mcp]>=1.4.0`, is in beta (importing raises a `LangChainBetaWarning` once per process) and is built on FastMCP. The docs link a migration guide from `langchain-mcp-adapters`.
- Prefer `MCPAdapter` for new code; the legacy client below is for code that already uses it.

## New: MCPAdapter
```python
from langchain.agents import create_agent
from langchain.mcp import MCPAdapter

async def main():
    async with MCPAdapter("https://example.com/mcp") as adapter:
        tools = await adapter.list_tools()
        agent = create_agent("<model-id>", tools)
        return await agent.ainvoke({"messages": [{"role": "user", "content": "..."}]})
```
- The tools hold the client, so the agent stays usable after the context exits (docs).
- The transport is inferred from the target: an http(s) URL string uses Streamable HTTP; a `Path` to a script is launched as a stdio subprocess; an in-process FastMCP server is connected in memory (good for tests); also a transport object, an `MCPConfig` dict (`{"mcpServers": {...}}`, several servers) or a prebuilt `fastmcp.Client`.
- A `str` target must be an http(s) URL. FastMCP would treat a string naming an existing file as a script to launch, so `MCPAdapter` rejects strings not shaped like a URL (matters when targets come from config or a model).
- Docs sub-pages cover tools, connections and authentication (bearer, OAuth 2.1, per-user); they were not read for this check.

## Legacy: MultiServerMCPClient (langchain-mcp-adapters)
```python
from langchain_mcp_adapters.client import MultiServerMCPClient

client = MultiServerMCPClient({
    "math": {"command": "python", "args": ["/abs/path/math_server.py"], "transport": "stdio"},
    "weather": {"url": "http://localhost:8000/mcp", "transport": "http",
                "headers": {"Authorization": "Bearer <token>"}},
})
tools = await client.get_tools()
agent = create_agent("<model-id>", tools)
```
- README examples use `transport` values `stdio`, `http` and `streamable_http`; `sse` is also mentioned. Only `sse` and `http`/`streamable_http` support the `headers` field, sent with every HTTP request.
- By default each tool invocation starts a new MCP `ClientSession`. To hold a session: `async with client.session("math") as session: tools = await load_mcp_tools(session)`.
- Tool errors: an MCP execution error (`isError=True`) comes back to the model as a `ToolMessage` with `status="error"` by default (`handle_tool_errors=True`) so the agent can self-correct; `handle_tool_errors=False` restores raising `ToolException`. Transport/session failures and content-conversion errors always raise.
- The README comments that stdio was designed for apps on a user's machine; think before using it in a web server and ask whether a plain `@tool` would do.
- With LangGraph: `ToolNode(tools)` works in a `StateGraph`; for a LangGraph API server, build the agent in an async `make_graph()` and point `langgraph.json` `graphs` at it.

## Practical advice (not from the pages above)
- Filter large tool lists to what the agent needs; treat MCP servers and their tool output as untrusted input; put destructive tools behind approval.

## Checked
Method: 2026-11-08 read both cited pages in full (the repo README raw file and the docs.langchain.com MCP page as markdown). The earlier modelcontextprotocol.io transports source was dropped unread. Rewritten: added the maintenance notice and `MCPAdapter`, removed the unsupported "current standard / legacy" transport labels and the `get_resources` / `get_prompt` claim (not in the sources), added headers and tool-error behaviour. Advice section is author guidance, unverified against the pages.
