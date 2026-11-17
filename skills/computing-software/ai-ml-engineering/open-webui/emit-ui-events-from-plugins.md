---
id: computing-software.ai-ml-engineering.open-webui.emit-ui-events-from-plugins
name: emit-ui-events-from-plugins
category: computing-software
field: ai-ml-engineering
product: open-webui
tags: [valves-events, events, event-emitter, event-call, status, embeds, persistence, open-webui]
level: practitioner
status: docs-checked
description: "Use __event_emitter__ and __event_call__ in Open WebUI plugins for status, citations, embeds and dialogs, and pick event names that persist after a tab closes."
sources:
  - https://docs.openwebui.com/features/extensibility/plugin/development/events
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: push progress, citations, embeds and prompts from a Tool, Pipe, Filter or Action to the chat UI.

## Two helpers
- `await __event_emitter__({"type": ..., "data": {...}})` is one-way. `chat_id` and `message_id` are filled in for you.
- `await __event_call__({...})` waits for the browser: types `confirmation` (data `title`, `message`), `input` (adds `placeholder`, `value`, optional `type: "password"`; `"input": {"type": "select", "options": [...]}` offers choices, and cancel returns `false`) and `execute` (data `code`, JavaScript run unsandboxed in the page via `new Function()`, may `return` a value). `execute` also works through the emitter as fire-and-forget; prefer that for blob downloads (iOS PWA two-way calls can fail with `TypeError: Load failed`).

## Common types
- `status`: `{description, done, hidden}`. Always finish with a status carrying `done: True`, otherwise the last line shimmers forever. `hidden: True` saves to `statusHistory` without showing.
- `notification`: `{type: "info"|"success"|"warning"|"error", content}`. Dropped for internal or background requests.
- `source` / `citation`: `{source: {name, id}, document: [passages], metadata: [{source, name, url}]}` (`document` and `metadata` are parallel lists).
- `embeds`: `{embeds: [html_or_url_strings], replace: False}`. Strings starting `http://`, `https://` or `//` load as URLs, anything else is raw HTML. Default merges newest first; `replace: True` overwrites (empty list clears). Use it for a live progress widget.
- `chat:message:delta` / `message` append; `chat:message` / `replace` overwrite; `files`; `chat:title` (data is the title string); `chat:tags` (data ignored; write tags to the DB first, then emit as a refresh signal); `chat:message:favorite` `{favorite: bool}`.

## Timeouts
`__event_call__` waits forever unless `WEBSOCKET_EVENT_CALLER_TIMEOUT` (seconds) is set. Failures are return values, not exceptions:
```python
r = await __event_call__({"type": "confirmation", "data": {"title": "Delete?", "message": "Cannot undo."}})
if isinstance(r, dict) and r.get("error"):
    return f"Could not ask the user: {r['error']}"
```
Errors: `Client session disconnected.` (immediate) or `Event call timed out. The browser tab may be inactive or closed.` If `execute` JS throws, no reply is sent and the call hangs until the timeout; wrap the code in try/catch and return an error value.

## Persistence after the tab closes
Server tasks keep running with no execution timeout; the stop button calls `POST /api/tasks/chat/{chat_id}/stop`. Only these short names are written to the DB by the emitter: `status`, `message`, `replace`, `embeds`, `files`, `source`/`citation` (untyped payload only). Aliases like `chat:message:embeds`, plus `notification`, `chat:title`, `chat:tags` and `chat:message:delta`, are Socket.IO only and lost. Nothing is saved for temporary chats or channel messages.

## Pipe gotcha
In a Pipe, deliver content by `return`/`yield`, not by `message` events: when the pipe finishes, the frontend saves its own history and can overwrite event-written content with empty text. Use events for status, sources, files, embeds. Actions: only an inline `HTMLResponse` is written server-side; a `{"messages": [...]}` return is saved only if the tab is open.

## Checked
2026-11-04. Confirmed against the Open WebUI docs page features/extensibility/plugin/development/events (read in full): the two helpers, confirmation, input (password, select, cancel returns false) and execute semantics including new Function() and the iOS PWA note, the status done and hidden behaviour, notification, source, embeds merge versus replace and the URL versus raw HTML rule, title, tags and favorite events, WEBSOCKET_EVENT_CALLER_TIMEOUT and both error strings, the persistence table and short-name rule, the stop endpoint, and the pipe and action caveats. Nothing removed.
Method: documentation only; no commands were run.
