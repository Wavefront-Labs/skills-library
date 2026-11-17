---
id: computing-software.ai-ml-engineering.open-webui.write-a-pipe-function
name: write-a-pipe-function
category: computing-software
field: ai-ml-engineering
product: open-webui
tags: [functions-pipe-filter-action, pipe, manifold, custom-model, valves, open-webui]
level: advanced
status: docs-checked
description: "Write an Open WebUI Pipe function that appears as a model, including manifold pipes(), streaming proxies, return-value rules and tool-call pitfalls."
sources:
  - https://docs.openwebui.com/features/extensibility/plugin/functions/pipe
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: add a custom "model" (proxy or agent) backed by Python code. Pipes run arbitrary code on the server and are admin-only; review code before importing.

## Skeleton (keep order: Valves, __init__, pipe)
```python
from pydantic import BaseModel, Field

class Pipe:
    class Valves(BaseModel):
        MODEL_ID: str = Field(default="")

    def __init__(self):
        self.valves = self.Valves()

    async def pipe(self, body: dict):
        return "Hello, World!"
```
Prefer `async def pipe`. A nested `UserValves` class gives per-user settings, delivered as `__user__["valves"]`; admin `Valves` reload from the DB on every request. Users see a Valves button in the chat input when the pipe is the only selected model, if admin or holding the Allow Chat Valves permission.

## pipe() signature
`body` is the chat completion request with `metadata` removed (for workspace models built on the pipe, `model` is rewritten to the pipe id and parameters/system prompt merged). Add any of `__user__`, `__request__`, `__event_emitter__`, `__event_call__`, `__chat_id__`, `__session_id__`, `__message_id__`, `__task__`, `__task_body__`, `__files__`, `__metadata__`, `__oauth_token__`, `__tools__` to receive them; `__event_emitter__`/`__event_call__` are `None` when the request has no session/chat/message ids (plain API calls).

## Return values
Streaming: `str` = one chunk; sync/async generator streamed per item (dict or Pydantic model as JSON, a str starting `data:` untouched, other str wrapped as chat chunk); Open WebUI appends `finish_reason: stop` and `data: [DONE]`. `StreamingResponse` forwarded as-is. Non-streaming: dict/StreamingResponse returned as-is, str or generator joined into one completion. An exception escaping `pipe()` shows as an error on the message; a returned `f"Error: {e}"` renders as normal assistant text.

## Multiple models (manifold)
```python
def pipes(self):   # may be async or a plain list attribute
    return [{"id": "model_id_1", "name": "model_1"}]
```
Model id becomes `<function id>.<id>` (split on the first dot, so `body["model"][body["model"].find(".")+1:]` yields the sub id). A class `name` attribute prefixes every sub-model name. If `pipes()` raises the function contributes no models; an entry without `id` or `name` skips the whole function. Function id must be a valid Python identifier, stored lowercase.

## Proxy streaming pattern
Use `httpx.AsyncClient` (not `requests`, which blocks the event loop); for `body.get("stream")` return an async generator that `yield`s `r.aiter_lines()` from `client.stream("POST", url, json=payload, headers=headers)`. Blocking libraries: `await anyio.to_thread.run_sync(...)`.

## Gotchas
- Self-contained agents must NOT emit `delta.tool_calls`: the middleware treats them as client tool requests and loops back into your pipe up to `CHAT_RESPONSE_MAX_TOOL_CALL_ITERATIONS` times. Yield `<details type="tool_calls" done="true" id=".." name=".." arguments="{html-escaped json}">` blocks instead.
- Internal helpers: `from open_webui.utils.chat import generate_chat_completion`, `from open_webui.models.users import Users`; call `await generate_chat_completion(__request__, body, user)`. Signatures can change between releases.
- Dependencies: frontmatter `requirements: pkg1, pkg2` (docstring must be the first line), installed on save unless `ENABLE_PIP_INSTALL_FRONTMATTER_REQUIREMENTS` is off or `OFFLINE_MODE` is on.
- Keep API keys in Valves, never hardcoded.

## Checked
2026-11-07. Confirmed against the Open WebUI docs: features/extensibility/plugin/functions/pipe (read in full). Nothing removed.
Method: documentation only; no commands were run.
