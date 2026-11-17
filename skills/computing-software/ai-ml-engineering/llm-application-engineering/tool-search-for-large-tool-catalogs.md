---
id: computing-software.ai-ml-engineering.llm-application-engineering.tool-search-for-large-tool-catalogs
name: tool-search-for-large-tool-catalogs
category: computing-software
field: ai-ml-engineering
product: llm-application-engineering
tags: [llm-application, tool-search, tool-use, defer-loading, mcp, context-engineering]
level: practitioner
status: docs-checked
description: "Scale agents to hundreds of tools with Claude tool search: defer_loading, regex vs BM25 search tools, tool naming for discoverability, caching, and custom retrieval of tools."
sources:
  - https://docs.claude.com/en/docs/agents-and-tools/tool-use/tool-search-tool
  - https://docs.claude.com/en/docs/agents-and-tools/tool-use/implement-tool-use
  - https://www.anthropic.com/engineering/advanced-tool-use
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Scaling to many tools with tool search

**Goal:** an agent with a large tool catalogue (many MCP servers, hundreds of internal APIs) keeps context small and picks the right tool reliably.

## Problem
Every tool definition costs input tokens on every request, and a typical multi-server setup can consume tens of thousands of tokens in definitions before any work starts (Anthropic's page cites about 55k for five servers).

## Claude tool search
Declare a search tool and mark rarely needed tools as deferred:
```python
tools = [
    {"type": "tool_search_tool_bm25_20251119", "name": "tool_search_tool_bm25"},
    {"name": "get_customer", "description": "...", "input_schema": {...}},          # always loaded
    {"name": "export_invoice_pdf", "description": "...", "input_schema": {...}, "defer_loading": True},
    # hundreds more with defer_loading: True
]
resp = client.messages.create(model=MODEL, max_tokens=4096, tools=tools, messages=msgs)
```
Deferred tools are not shown to the model up front. When it needs a capability it calls the search tool; the API returns matching tools as `tool_reference` blocks (up to 5 by default) and they are expanded for the model to call. You still send every tool definition in the `tools` array on each request; `defer_loading` controls what enters context.
- `tool_search_tool_regex_20251119`: the model writes regex patterns over tool names/descriptions - precise when names are systematic.
- `tool_search_tool_bm25_20251119`: natural-language queries - better for descriptive catalogues.
- Rules: never set `defer_loading` on the search tool itself, and at least one tool must stay non-deferred.
- Keep your 3-5 most frequently used tools non-deferred so Claude can call them without searching first.

## Make tools findable
- Use consistent namespacing in tool names: prefix by service or resource (for example `github_`, `slack_`) so one search matches the whole group.

## Alternatives
- Your own client-side search (for example embeddings): return standard `tool_result` content with `tool_reference` blocks from a custom tool.
- Programmatic tool calling lets Claude invoke tools from a code execution environment, reducing the impact on the context window (Anthropic's advanced tool use post).

## Caching
A tool with `defer_loading: true` cannot also carry `cache_control` (the API returns a 400); put the cache breakpoint on a non-deferred tool.

## Verify
- [ ] Input tokens per request dropped versus loading all tools.
- [ ] Tool-selection accuracy on an eval set equal or better than the all-tools baseline.
- [ ] Common tasks complete without an extra search round-trip.

## Checked
2026-11-01. Confirmed against Anthropic's tool search tool page: tool type names with 20251119 suffix, regex and BM25 behaviour, `defer_loading`, non-deferred rules, `tool_reference` blocks, 3-5 non-deferred tools, namespacing, custom client-side search, `cache_control` 400 rule; and the advanced tool use post (programmatic tool calling). Removed: model id, selection-accuracy claim, sub-agent routing and cache-write claims.
Method: documentation only; no commands were run.
