---
id: computing-software.data-engineering.polars.llm-polars-code-generation
name: llm-polars-code-generation
category: computing-software
field: data-engineering
product: polars
tags: [polars-llm-codegen, llm, mcp-server, system-prompt, web-search, few-shot-examples, group-by, agent-skill]
level: practitioner
status: docs-checked
description: "Make LLMs emit valid Polars rather than pandas: official skill, remote MCP server config, system prompt, web search and in-prompt examples such as group_by."
sources:
  - https://docs.pola.rs/user-guide/misc/polars_llms/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Get LLMs to write valid Polars

Problem: LLMs sometimes return pandas code or invalid Polars. These approaches come from community testing of model responses.

## 1. Official Polars skill
The Polars skill for Agents (repository linked on the page) loads Polars expertise into the agent so it writes more idiomatic Polars and can translate pandas to Polars. See that repository for installation.

## 2. Polars MCP server
A remote Model Context Protocol server exposes the official Polars documentation so an LLM can query the user guide and API reference. Config:
```json
{
  "mcpServers": {
    "ask_polars": {
      "command": "npx",
      "args": ["mcp-remote", "https://mcp.pola.rs/mcp"]
    }
  }
}
```
Refer to your client's documentation for connecting to an MCP server. Report problems or missing features on the public issue tracker.

## 3. System prompt
State a default such as "Use Polars as the default dataframe library". This typically makes models consistently generate Polars instead of pandas. Set it in the settings of web LLMs like ChatGPT and IDE LLMs like Cursor. Common examples like `df.group_by("a").agg(pl.col("b").mean())` can also go in the system prompt for consistency.

## 4. Enable web search
Lets the model reference current Polars docs. Some IDE LLMs index API docs (in Cursor, add Polars as a custom docs source and tell the agent to use it). Caveat: web search does not guarantee valid code; a model confident from pre-training may ignore the results. The Polars API pages also have AI-enabled search.

## 5. Provide examples
A bare prompt such as
```python
df = pl.DataFrame({"id": ["a","b","a","b","c"], "score": [1,2,1,3,3], "year": [2020,2020,2021,2021,2021]})
# Compute average of score by id
```
often yields outdated `groupby` rather than `group_by`. Adding a comment with a docs example (`# df.group_by("a").agg(pl.col("b").mean())`), preferably with web search on, produces valid output more often. Web search plus examples beats either alone; an example that contradicts the model's expectation seems more likely to trigger a search. Explicit instructions such as "use `group_by` instead of `groupby`" also help.

## Checked
2026-11-07: every claim compared with the cited Polars user guide page(s). Removed or trimmed claims the cited page does not confirm.

Method: documentation only; no commands were run.
