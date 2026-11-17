---
id: computing-software.ai-ml-engineering.open-webui.write-an-idempotent-request-filter
name: write-an-idempotent-request-filter
category: computing-software
field: ai-ml-engineering
product: open-webui
tags: [functions-pipe-filter-action, filter, request-hook, idempotent, tool-loop, open-webui]
level: advanced
status: docs-checked
description: "Use the Filter request hook to enforce changes on every outgoing model call in Open WebUI, and write it idempotent so tool loops do not duplicate edits."
sources:
  - https://docs.openwebui.com/features/extensibility/plugin/functions/filter
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: stamp or redact on the wire for every provider call, not just once per turn.

## inlet vs request
`inlet` runs once per user turn. `request(self, body, __user__=None)` runs immediately before EVERY call to the model provider, including each hop of a tool loop and the call after an approved tool run (request filters run before the approved tool executes, so a filter can still reject it). Use `inlet` for per-turn effects (billing, rate limiting, logging a turn); use `request` for enforcement (stamping a parameter, redaction). Things added in `inlet` can vanish from later hops when the message list is rebuilt.

## What the body contains in request
Popped before `request`: `features`, `tool_ids`, `terminal_id`, `files`, `folder_id`, `skill_ids` (so read those in `inlet`); `variables`, `regeneration_prompt` and `params` are popped even before `inlet` (`variables` stays at `__metadata__["variables"]`). `features` is available as the `__features__` reserved arg on the first call only (give it a default). Present only at request time: retrieved RAG chunks wrapped in `<source>` tags, the resolved `tools` array, chat and folder system prompts, memory and web-search context. So `request` can rewrite retrieved chunk text without `file_handler`. The workspace model's own System Prompt is added after `request` returns, and provider-shape normalization also happens after.

## Idempotence (the common bug)
Each hop passes the whole conversation through your filter again.
```python
# RIGHT
async def request(self, body: dict) -> dict:
    marker = "Be concise."
    if not any(m.get("role") == "system" and marker in str(m.get("content", ""))
               for m in body["messages"]):
        body["messages"].insert(0, {"role": "system", "content": marker})
    return body
```
Test for containment, not equality: before each call Open WebUI merges all system messages into one. Clamping, downscaling and regex redaction are naturally idempotent; append/prepend/increment need a guard.

## Costs and errors
Expensive work repeats per hop and per full history; cache on a content hash. Exceptions: first `request` of a turn aborts the turn; on a later hop it ends the tool loop with an error (streamed text stays). Catch and return the body unchanged if you prefer to degrade. `file_handler` does nothing for `request` filters. A filter without `request` is unaffected.

## Checked
2026-11-07. Confirmed against the Open WebUI docs: features/extensibility/plugin/functions/filter (read in full). Nothing removed.
Method: documentation only; no commands were run.
