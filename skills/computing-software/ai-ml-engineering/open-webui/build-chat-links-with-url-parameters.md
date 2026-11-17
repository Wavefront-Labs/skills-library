---
id: computing-software.ai-ml-engineering.open-webui.build-chat-links-with-url-parameters
name: build-chat-links-with-url-parameters
category: computing-software
field: ai-ml-engineering
product: open-webui
tags: [open-webui, chat-features, url-parameters, deep-links, temporary-chat]
level: practitioner
status: docs-checked
description: "Compose Open WebUI chat links that preselect models, tools, web search, voice, a prompt or a settings tab using URL query parameters, and know the confirmation and tool-ID rules."
sources:
  - https://docs.openwebui.com/features/chat-conversations/chat-features/url-params
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Build chat links with URL parameters

Goal: open a chat already configured for a task, from a bookmark, wiki or script.

## Parameters
| Param | Effect |
|---|---|
| `models=a,b` / `model=a` | preselect models (passing either suppresses the fallback to group or `DEFAULT_MODELS`) |
| `q=Hello%20there` | puts text in the input; user sends it |
| `web-search=true` | web search on |
| `code-interpreter=true` | code interpreter on for next prompt |
| `image-generation=true` | image generation on |
| `tools=` or `tool-ids=` | comma-separated tool IDs |
| `youtube=VIDEO_ID` | transcribe a video, after confirmation |
| `load-url=https://...` | fetch a page as a document, after confirmation |
| `call=true` / `voice=true` | start Voice Mode, after confirmation |
| `temporary-chat=true` | disposable chat, no history |
| `settings=admin:documents` | open settings on a tab |

Combined example: `/?models=model1&youtube=VIDEO_ID&web-search=true&tools=tool1,tool2&call=true&q=Hello%20there&temporary-chat=true`. One **Open link** dialog lists the YouTube/load-url targets and the voice call; cancelling loads nothing.

## Tool IDs
Use the internal ID, not the display name. A workspace tool uses its plain ID (`/?tools=my_workspace_tool`). Tool servers are prefixed: `server:mcp:<server-id>` for MCP, `server:<server-id>` for OpenAPI (an OpenAPI connection with no ID uses its list position starting at 0), e.g. `/?tool-ids=server:mcp:my_mcp_server`. A non-matching ID is silently not activated.

## Voice call preconditions
The user needs the Allow Call permission, exactly one model selected, and in Standard call mode an STT engine other than Web API.

## Settings tabs
User: general, interface, notifications, shortcuts, connections, tools, personalization, audio, data_controls, usage, archived_chats, account, about. Admin as `admin:<tab>`: general, authentication, connections, models, subagents, evaluations, analytics, integrations, documents, web, code-execution, interface, audio, images, db, pipelines. A non-admin following an `admin:` link lands on General.

## Notes prefill
`/notes/new?title=Meeting&content=Agenda%3A` opens a confirm dialog before creating the note; title defaults to today's date.

## Temporary chat limits
Nothing is stored, so task lists, per-chat terminals, sub-agents, timers and forking are unavailable (no `/fork`; typing it answers "No chat to fork"). Document parsing is frontend-only (complex DOCX may not parse). Other tools, memory, notes and web search still work; disable tools on the model if unwanted.

## Checked
2026-11-04. Confirmed against the Open WebUI docs page features/chat-conversations/chat-features/url-params (read in full): every parameter, the model fallback note, tool ID prefixes, voice call preconditions, settings tab lists, notes prefill, combined example and the temporary chat limits. Nothing removed.
Method: documentation only; no commands were run.
