---
id: computing-software.ai-ml-engineering.open-webui.emit-events-from-external-tool-servers
name: emit-events-from-external-tool-servers
category: computing-software
field: ai-ml-engineering
product: open-webui
tags: [valves-events, events, openapi-tools, mcp, rest-api, service-account, open-webui]
level: advanced
status: docs-checked
description: "Let an OpenAPI or MCP tool server push status, citations and embeds into an Open WebUI chat through the message event endpoint with a service-account key."
sources:
  - https://docs.openwebui.com/features/extensibility/plugin/development/events
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: external tool servers cannot use `__event_emitter__`; they post events over REST.

## 1. Get the chat and message ids
Set `ENABLE_FORWARD_USER_INFO_HEADERS=True` on Open WebUI. Calls to tool servers then carry `X-OpenWebUI-Chat-Id` and `X-OpenWebUI-Message-Id` (rename with `FORWARD_SESSION_INFO_HEADER_CHAT_ID` / `FORWARD_SESSION_INFO_HEADER_MESSAGE_ID`). The flag also ships the user's email, name and role to every backend. Narrower alternative for a global tool server: add a connection custom header using the placeholders `{{CHAT_ID}}` and `{{MESSAGE_ID}}`; these are interpolated regardless of the flag. Custom headers are not sent for user-added tool servers (the browser calls those directly).

## 2. Hold your own key
Open WebUI never forwards a user API key or session token (no `{{API_KEY}}` or `{{TOKEN}}` placeholder exists). The endpoint requires the caller to be the chat owner or an admin, so create a dedicated admin or service-account user, generate an API key for it and store it as a secret on the tool server. One admin key serves all users' chats; the forwarded ids say which message to target.

## 3. Post the event
```python
import httpx
httpx.post(
  f"http://openwebui-host/api/v1/chats/{chat_id}/messages/{message_id}/event",
  headers={"Authorization": f"Bearer {api_key}"},
  json={"type": "status", "data": {"description": "Working...", "done": False}})
```
Supported types: `status`, `notification`, `chat:message:delta`/`message`, `chat:message`/`replace`, `files`, `embeds` (with `data.replace: true` to overwrite), `source`/`citation` (this is how an MCP search tool attaches citations, including in native function-calling mode). Finish status sequences with `done: true`.

## Limits
`input`, `confirmation` and two-way `execute` need a WebSocket reply channel and are not supported for external tools. Fire-and-forget `execute` may work depending on setup. Persistence follows the short-name rule: send `embeds`, `status`, `message`, `replace`, `files`, `source` to have them saved; aliases and `notification` are not.

## Checked
2026-11-04. Confirmed against the Open WebUI docs page features/extensibility/plugin/development/events (read in full): ENABLE_FORWARD_USER_INFO_HEADERS and the two header names with their override variables, the custom header placeholder alternative and the user-added tool server caveat, no forwarding of user credentials, the owner-or-admin check, the event endpoint path, the supported type list, the unsupported interactive types, and the persistence short-name rule. Nothing removed.
Method: documentation only; no commands were run.
