---
id: computing-software.ai-ml-engineering.llm-application-engineering.server-tools-web-search-fetch-code-execution
name: server-tools-web-search-fetch-code-execution
category: computing-software
field: ai-ml-engineering
product: llm-application-engineering
tags: [llm-application, server-tools, web-search-tool, web-fetch, code-execution, claude-api, pause-turn]
level: practitioner
status: docs-checked
description: "Use Anthropic server tools: web_search and web_fetch type versions, domain filters, max_uses, code execution results, errors returned as 200 blocks and pause_turn."
sources:
  - https://docs.claude.com/en/docs/agents-and-tools/tool-use/web-search-tool
  - https://docs.claude.com/en/docs/agents-and-tools/tool-use/web-fetch-tool
  - https://docs.claude.com/en/docs/agents-and-tools/tool-use/code-execution-tool
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Server tools: web search, web fetch, code execution

Server tools run on Anthropic's infrastructure: declare them in `tools`, results come back as content blocks in the same response. No execution loop on your side.

## Declare
```python
resp = client.messages.create(
    model=MODEL_ID, max_tokens=16000,
    tools=[{"type": "web_search_20260209", "name": "web_search", "max_uses": 5,
            "allowed_domains": ["example.com"]},
           {"type": "web_fetch_20260209", "name": "web_fetch", "max_uses": 3, "citations": {"enabled": True}}],
    messages=[{"role": "user", "content": "Summarise recent changes to <topic>."}])
```
- `_20260209` and later variants add dynamic filtering (Claude writes and runs code to filter results before they reach context; documented for Claude 4.6 and later); `web_search_20250305` / `web_fetch_20250910` are the basic versions. Platform availability differs (on Microsoft Foundry deployments hosted on Azure only basic web fetch is supported).
- With dynamic filtering the API provisions code execution automatically: you do not need to add the code execution tool yourself.
- `allowed_domains` or `blocked_domains` (not both); `user_location` localizes search.
- Web fetch only fetches URLs already present in the conversation (user messages, client-side tool results, earlier search or fetch results), not URLs appearing only in Claude's own output.
- Code execution: take the current `type` string from the code execution tool page; results arrive as `bash_code_execution_tool_result` blocks with `stdout`/`stderr`/`return_code`.

## Results and errors
- Search results: `web_search_tool_result` with a **list** of results; answer text blocks carry citations.
- Errors do not raise: the result block's `content` is an **object** with `error_code` (e.g. `max_uses_exceeded`). Branch on list vs object before indexing.
- `stop_reason == "pause_turn"`: a long server-tool turn was paused; send the paused assistant message back unchanged in a new request to continue.

## Cost and safety
See the vendor's pricing page for billing; cap `max_uses` (web fetch has no default limit). Fetched pages are untrusted input (prompt injection): keep high-impact tools behind approval in the same conversation.

## Verify
- [ ] Log number of searches/fetches per request and citation coverage of the final answer.

## Checked
2026-11-01. Confirmed on the web search and web fetch tool pages: tool type versions, `max_uses` and `max_uses_exceeded`, `allowed_domains`/`blocked_domains` (not both), `user_location`, dynamic filtering, `pause_turn`, fetch URL restrictions. Removed: model id, code execution type string, billing description, per-platform claim for Vertex AI.
Method: documentation only; no commands were run.
