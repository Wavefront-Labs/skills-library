---
id: computing-software.ai-ml-engineering.ollama.capability-web-search-fetch
name: capability-web-search-fetch
category: computing-software
field: ai-ml-engineering
product: ollama
tags: [web-search, web-fetch, max-results, search-agent]
level: practitioner
status: docs-checked
description: "Call Ollama's hosted web_search and web_fetch APIs with a bearer key and use them as tools in a small search agent."
sources:
  - https://docs.ollama.com/capabilities/web-search.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: give a model current web information.

An Ollama account and API key (ollama.com/settings/keys) are required; set `OLLAMA_API_KEY`.

Search: `POST https://ollama.com/api/web_search` with `query` (required) and `max_results` (optional; default 5, maximum 10). The response has `results`, each with `title`, `url` and `content` (a snippet).

```
curl https://ollama.com/api/web_search \
  --header "Authorization: Bearer $OLLAMA_API_KEY" \
  -d '{"query": "what is ollama?"}'
```

Fetch: `POST https://ollama.com/api/web_fetch` with `url` (required). The response has `title`, `content` and `links`.

Libraries: Python has `ollama.web_search(...)` and `ollama.web_fetch(...)`; JavaScript has `client.webSearch(query)` and `client.webFetch(url)`. For an agent, pass both functions as tools to `chat` (the example uses `qwen3:4b` with `think=True`) and loop on `tool_calls`, appending `role: tool` messages with `tool_name`.

Context: results can run to thousands of tokens. The page recommends raising the model context to at least about 32000 tokens, and says search agents work best at full context length; Ollama's cloud models run at full context. The example agent truncates tool results (to 8000 characters) for limited context lengths.

The page also describes an MCP server (a Python example script) for using web search in MCP clients such as Cline, Codex and Goose.

## Checked

Method: 2026-11-08 read the full web search page. Removed the unsupported claim about a 64000-token recommendation on another page; added the JavaScript webSearch call and MCP note.
