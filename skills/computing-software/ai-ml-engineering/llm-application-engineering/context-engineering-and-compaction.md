---
id: computing-software.ai-ml-engineering.llm-application-engineering.context-engineering-and-compaction
name: context-engineering-and-compaction
category: computing-software
field: ai-ml-engineering
product: llm-application-engineering
tags: [llm-application, agents, context-engineering, context-compaction, context-editing, memory-tool, long-running-agents]
level: practitioner
status: docs-checked
description: "Manage context for long-running agents: lean system prompts and tools, just-in-time retrieval, server-side compaction and context editing on Claude, memory files and sub-agents."
sources:
  - https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
  - https://docs.claude.com/en/docs/build-with-claude/compaction
  - https://docs.claude.com/en/docs/build-with-claude/context-editing
  - https://docs.claude.com/en/docs/agents-and-tools/tool-use/memory-tool
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Context engineering and compaction for long-running agents

Context is a finite attention budget: as it fills, recall of earlier details degrades ("context rot"), cost rises and latency grows. Goal: the smallest set of high-signal tokens that lets the model act correctly at each step.

## What goes in
- **System prompt:** clear, at the right altitude (principles and heuristics, not brittle if-else lists), organised in sections.
- **Tools:** few, non-overlapping, token-efficient results (see tool design). Tool search / deferred loading for large catalogues.
- **Examples:** a few diverse canonical ones, not every edge case.
- **Data:** retrieve just in time - give the agent search/read tools and lightweight references (file paths, ids, URLs) instead of pre-loading everything.

## Keeping long runs bounded (Claude API)
**Context editing** (beta `context-management-2025-06-27`) clears stale tool results automatically:
```python
client.beta.messages.create(model=MODEL_ID, max_tokens=16000, betas=["context-management-2025-06-27"],
    context_management={"edits": [{"type": "clear_tool_uses_20250919"}]}, tools=tools, messages=messages)
```
**Server-side compaction** (beta) has Claude write a summary on the server that replaces older turns. The API offers compaction on demand (you decide when) and compaction at a token threshold (the API decides); each has its own beta header, so read the compaction overview for the current header and parameters. Context editing instead clears old tool results or thinking blocks by rule rather than summarising.

Elsewhere (other providers, frameworks): summarise at thresholds yourself, preserving decisions, open tasks, ids and file paths verbatim; drop raw tool outputs already acted upon.

## Structured note-taking and memory
- The agent maintains a progress file (`NOTES.md`, todo list, test status JSON) and re-reads it after compaction or in a fresh session.
- Claude's memory tool (`{"type": "memory_20250818", "name": "memory"}`) gives a client-side file directory the model can read/write across conversations; you implement the storage backend and must sandbox paths.
- Git history and test results are durable state for coding agents.

## Sub-agents
Delegate exploration to sub-agents with clean contexts; they return condensed findings instead of their whole search trail. Keeps the lead agent's context focused.

## Caching interplay
Clearing tool results invalidates cached prompt prefixes; use `clear_at_least` so each clear frees enough tokens to be worth the cache rewrite, and keep thinking blocks if you want cache hits.

## Verify
- [ ] Long-task eval (many tool calls) passes with editing/compaction on; tokens per task and success rate compared to baseline.
- [ ] After a compaction, the agent still knows the task goal and open items (spot-check transcripts).

## Checked
2026-11-01. Confirmed against the Anthropic context-engineering essay (context rot, attention budget, just-in-time retrieval, NOTES.md, sub-agents), the compaction overview (server-written summary, on-demand vs threshold, separate betas), the context editing page (`context-management-2025-06-27`, `clear_tool_uses_20250919`, `clear_at_least`, cache invalidation) and the memory tool page (client-side, `memory_20250818`). Removed: model id, compaction beta id and default threshold, sub-agent token figure.
Method: documentation only; no commands were run.
