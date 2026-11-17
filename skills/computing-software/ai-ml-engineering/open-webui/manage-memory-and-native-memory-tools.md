---
id: computing-software.ai-ml-engineering.open-webui.manage-memory-and-native-memory-tools
name: manage-memory-and-native-memory-tools
category: computing-software
field: ai-ml-engineering
product: open-webui
tags: [open-webui, memory, native-function-calling, permissions, personalization]
level: practitioner
status: docs-checked
description: "Enable and administer Open WebUI memory: native memory tools, the admin and permission toggles, background review, injection limits and the blank-reply gotcha."
sources:
  - https://docs.openwebui.com/features/chat-conversations/memory
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Manage memory and the native memory tools

Goal: let models remember facts across chats, with admin control over who gets it.

## User side
Settings > Personalization > Memory: add, edit, delete memories manually. Everything a model adds is reviewable and deletable there. Memories live in the Open WebUI database, scoped per user.

## Let the model manage memory (Native mode)
1. Memory enabled globally (below) and you have the permission.
2. Settings > Admin > Models > Edit model > Advanced Params: Function Calling = Native.
3. Workspace > Models > Edit > Builtin Tools: **Memory** category on (default).
4. Use a recent tool-capable model; very small models store inconsistently.
Tools: `add_memory` (type `user` or `context`, optional `path`), `update_memory` (batch add/replace/move/remove), `replace_memory_content` and `delete_memory` (by `id`), `search_memories` (default 5 results), `list_memories`, `list_memory_paths`, `read_memory_path`. Paths such as `work/projects` group memories. Automations also get these tools when memory is on for the owning user.

## Admin controls
- Global: Settings > Admin > General > Features > **Memories**, or `ENABLE_MEMORIES` (default True). Off hides Personalization, blocks the API and tools, stops injection.
- Per role/group: Admin Panel > Users > Permissions > Features > **Memories**, or `USER_PERMISSIONS_FEATURES_MEMORIES` (default True). Removal gives 403 on memory APIs and stops injection server-side even if a client sends `features: {"memory": true}`. Admins are exempt.
- `ENABLE_MEMORY_SYSTEM_CONTEXT` (default True; Settings > Admin > General > Memory System Context): turn off prompt injection while keeping the tools.
- `ENABLE_MEMORY_BACKGROUND_REVIEW` (default off) reviews recent turns every `MEMORIES_REVIEW_INTERVAL_TURNS` (default 10).
- Injection budgets `MEMORIES_CONTEXT_CHAR_LIMIT` and `MEMORIES_USER_CHAR_LIMIT`, both default 2000 characters.

## Gotcha
Memory is a native tool call, so the connection must stream OpenAI-schema tool calls. Endpoints that omit the `index` field on streamed tool calls (notably Google's OpenAI compatibility layer) drop the call and return occasional empty assistant messages with nothing in the logs.

## Checked
2026-11-04. Confirmed against the Open WebUI docs page features/chat-conversations/memory (read in full): manual management path, the four enabling steps and the weak-model caution, all eight tools with their parameters and the default of 5 search results, paths, the Automations note, the global toggle and ENABLE_MEMORIES default, the permission and USER_PERMISSIONS_FEATURES_MEMORIES default with the 403 and server-side injection behaviour and admin exemption, ENABLE_MEMORY_SYSTEM_CONTEXT, background review defaults, the 2000 character budgets, local per-user storage and the blank-reply warning about the missing index field. Nothing removed.
Method: documentation only; no commands were run.
