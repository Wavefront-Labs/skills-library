---
id: computing-software.ai-ml-engineering.open-webui.write-an-action-function-button
name: write-an-action-function-button
category: computing-software
field: ai-ml-engineering
product: open-webui
tags: [functions-pipe-filter-action, action, message-toolbar, event-call, multi-action, open-webui]
level: practitioner
status: docs-checked
description: "Write an Open WebUI Action function that adds a message-toolbar button, confirms with the user, rewrites a message and orders buttons with a priority valve."
sources:
  - https://docs.openwebui.com/features/extensibility/plugin/functions/action
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: add a clickable button under assistant messages that runs server-side Python. Admin-managed; arbitrary code, so review before importing. Always define it `async`.

## Skeleton
```python
from pydantic import BaseModel

class Action:
    class Valves(BaseModel):
        priority: int = 0   # lower = leftmost button

    def __init__(self):
        self.valves = self.Valves()

    async def action(self, body: dict, __user__=None, __event_emitter__=None, __event_call__=None):
        ok = await __event_call__({"type": "confirmation",
            "data": {"title": "Process Message", "message": "Enhance this message?"}})
        if not ok:
            return None
        msg = body["messages"][-1]
        return {"messages": [{"id": body["id"], "content": f"Enhanced: {msg.get('content', '')}"}]}
```

## Parameters
`body` has `messages` (each with `id`, `role`, `content`, `timestamp`, optionally `info`/`sources`), `model`, `chat_id`, `session_id`, and `id` = the message the button was pressed on. No attachments travel with it (fetch files through the file APIs using `body["chat_id"]`). Also available: `__user__` (dict, with `valves` when `UserValves` exist), `__event_emitter__`, `__event_call__`, `__model__`, `__request__`, `__id__`.

## Return value
Only `{"messages": [{"id": <existing message id>, ...fields to overwrite}]}` changes the chat. A bare `{"content": "..."}` silently does nothing; a returned `files` list does nothing. An `HTMLResponse` with `Content-Disposition: inline` becomes a Rich UI embed. Returning nothing is fine for side-effect actions.

## Events
```python
await __event_emitter__({"type": "status", "data": {"description": "Processing..."}})
await __event_emitter__({"type": "notification", "data": {"type": "info", "content": "Done"}})
resp = await __event_call__({"type": "input", "data": {"title": "Enter Value", "message": "...", "placeholder": "..."}})
```
If the browser cannot answer (tab gone, or `WEBSOCKET_EVENT_CALLER_TIMEOUT` expires) `__event_call__` returns a dict with an `error` key instead of raising; check for it.

## Multiple buttons
`actions` must be a class attribute or set on `self` in `__init__` (a module-level list is ignored):
```python
actions = [{"id": "summarize", "name": "Summarize", "icon_url": "https://example.com/s.svg"},
           {"id": "translate", "name": "Translate", "icon_url": "https://example.com/t.svg"}]
async def action(self, body, __id__=None, **kw): ...
```
`__id__` is the sub id only (no dots allowed in sub ids). Icon fallback: sub icon_url, frontmatter icon_url, class `icon_url`/`icon`, default.

## Enablement and order
Turn on the function's global toggle, or enable it per model in model settings. Non-admins can use it only on models they can access and chats they own. `ENABLE_PLUGINS=false` or `ENABLE_FUNCTIONS=false` disables actions. Buttons sort by `priority` valve ascending, ties alphabetical by function id.

## Frontmatter
Docstring at file top: `title`, `author`, `version`, `required_open_webui_version`, `icon_url`, `requirements`. Use a hosted `icon_url`, never base64: icon data ships in `/api/models` for every model with the action enabled (a 500 KB icon on 20 models adds ~10 MB per load).

## Gotchas
- The action runs inline in the HTTP request; no background hook. Report progress with status events.
- An exception escaping `action()` yields HTTP 400, a toast and an error marker on the message. Catch and notify instead.

## Checked
2026-11-07. Confirmed against the Open WebUI docs: features/extensibility/plugin/functions/action (read in full). Nothing removed.
Method: documentation only; no commands were run.
