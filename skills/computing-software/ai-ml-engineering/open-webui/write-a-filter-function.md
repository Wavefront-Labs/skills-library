---
id: computing-software.ai-ml-engineering.open-webui.write-a-filter-function
name: write-a-filter-function
category: computing-software
field: ai-ml-engineering
product: open-webui
tags: [functions-pipe-filter-action, filter, inlet, outlet, stream, api-outlet-filters, open-webui]
level: practitioner
status: docs-checked
description: "Write an Open WebUI Filter with inlet, stream and outlet hooks to rewrite user messages or replies, including API-caller behaviour and Responses API streams."
sources:
  - https://docs.openwebui.com/features/extensibility/plugin/functions/filter
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: change what goes to the model (inlet) and what comes back (stream chunks, outlet). Filters run arbitrary Python and are admin-created only.

## Skeleton
```python
from pydantic import BaseModel
from typing import Optional

class Filter:
    class Valves(BaseModel):
        pass
    def __init__(self):
        self.valves = self.Valves()
    async def inlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
        body["messages"][-1]["content"] = body["messages"][-1]["content"].replace("!!!", "").strip()
        return body
    async def stream(self, event: dict) -> dict:
        return event
    async def outlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
        return body
```
Always return the body/event: the return value feeds the next filter; `None` breaks the chain. Insert context with `body.setdefault("messages", []).insert(0, {"role": "system", "content": "..."})`.

## inlet
Runs once per user turn, before RAG retrieval (so `body["files"]` / `body["metadata"]["files"]` hold only references, not chunk text). Extra top-level fields you add (e.g. `body["safety_identifier"] = sha256(user id)`) are forwarded to the provider; `metadata`, `features`, `tool_ids`, `files`, `skill_ids` are stripped. Filters cannot inject HTTP headers (use the connection's header setting). You may append OpenAI-style tools to `body.setdefault("tools", [])`; they merge with server-resolved tools, but caller-provided `tools` make Open WebUI skip server-side tool resolution.

## stream (per chunk, since 0.5.17)
```python
async def stream(self, event: dict) -> dict:
    for choice in event.get("choices", []):
        delta = choice.get("delta", {})
        if "content" in delta:
            delta["content"] = delta["content"].replace("X", "")
    return event
```
On Responses-API connections, events are typed (`response.output_text.delta`, `.done`, `response.content_part.done`, `response.output_item.done`, `response.completed`); later events repeat the full text and overwrite your edit, so rewrite every event that carries text. A raise drops that event in the WebUI path (losing `response.completed` loses usage); a direct API streaming caller has the whole stream ended. Valves are resolved once per response.

## outlet
`body["messages"]` holds the whole chat; only the finished reply has `finish_reason` (`stop`, `length`, `tool_calls`). To change a reply edit both `content` and the text in `output` (items of type `message`, parts of type `output_text`), since the chat renders from `output`. Prefer logging; heavy rewriting belongs in a Pipe.

## Reserved args (declare only what you need)
`__model__` (base model at `__model__["info"]["base_model_id"]`), `__user__`, `__metadata__`, `__event_emitter__`, `__event_call__`, `__chat_id__`, `__message_id__`, `__oauth_token__`, `__id__`, `__request__`, and `__body__` (stream only). `__metadata__` is shared between inlet and outlet of the same request, so stash a start time there.

## Direct API callers
inlet/request/stream behave the same. outlet runs by default for `/api/chat/completions` (controlled by `ENABLE_API_OUTLET_FILTERS`, default True), but does not rewrite the HTTP response body. To get filtered output call `POST /api/chat/completed` with `model`, `messages` (including the assistant reply), `id`, `chat_id` (a chat you own, or empty) and `session_id`; errors come back as HTTP 400. Detect WebUI vs API with `metadata.get("chat_id") and metadata.get("session_id")`. In stream()/outlet() `__event_emitter__` is None for pure API callers.

## Gotchas
- Exceptions: inlet aborts the turn; stream drops the event (WebUI path); outlet is logged at debug and ignored (400 via `/api/chat/completed`).
- Dropdown valves: `Field("x", json_schema_extra={"enum": [...]})`.

## Checked
2026-11-07. Confirmed against the Open WebUI docs: features/extensibility/plugin/functions/filter (read in full). Qualified the stream-event raise behaviour to the WebUI path versus direct API callers.
Method: documentation only; no commands were run.
