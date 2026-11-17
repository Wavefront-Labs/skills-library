---
id: computing-software.ai-ml-engineering.open-webui.setup-rag-file-context-and-builtin-tools
name: setup-rag-file-context-and-builtin-tools
category: computing-software
field: ai-ml-engineering
product: open-webui
tags: [open-webui, rag, file-context, builtin-tools, native-function-calling, knowledge]
level: advanced
status: docs-checked
description: "Choose per-model File Context and Builtin Tools settings in Open WebUI to get injected RAG, agentic retrieval or none, and avoid the silent no-retrieval combination."
sources:
  - https://docs.openwebui.com/features/chat-conversations/rag
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Choose File Context and Builtin Tools per model

Goal: decide how attached files and knowledge bases reach a model.

## The two capabilities (per model)
- **File Context** (default on): RAG on attached files, content injected into context. The toggle only appears when File Upload is enabled for the model.
- **Builtin Tools** (default on): unless the model is Legacy, it receives tools such as `query_knowledge_bases`, `view_knowledge_file`, `search_chats`.

## Combinations (files or knowledge attached in the chat, Default or Native function calling)
| File Context | Builtin Tools | Result |
|---|---|---|
| on | on | Full agentic: injected content plus on-demand knowledge queries |
| on | off | Traditional RAG, injected upfront only |
| off | on | Tools-only: nothing pre-injected; Files tools `list_chat_files`, `query_chat_files`, `grep_chat_files`, `view_file` are injected; also the prompt-caching optimum |
| off | off | Files ignored entirely |

On Legacy function calling, Builtin Tools has no effect on chat attachments; File Context alone decides (on = injected, off = nothing).

## Knowledge attached to a model or folder differs
- Legacy: injected upfront if File Context is on.
- Default/Native: nothing is injected whatever File Context says; the model must use the builtin knowledge tools.
- Trap: File Context on + Builtin Tools off + Default function calling means model or folder knowledge is never reached. Fix by enabling Builtin Tools on that model, setting Function Calling to Legacy, or attaching the knowledge in the chat instead.

## Other levers
- "Using Entire Document" toggle per file or knowledge base injects the whole file into every message. Set the default in Settings > Interface > File > **Default Upload Mode**.
- `ENABLE_KB_EXEC=True` (off by default) gives capable models a shell-style interface (`ls`, `tree`, `grep`, `cat`, `head`/`tail`, pipes) over knowledge bases; needs native function calling, no effect on Legacy.
- Disable Builtin Tools for small models that cannot handle the `tools` parameter.
- Temporary Chat limits parsing to frontend-only, so complex DOCX files may show as raw data.

## Checked
2026-11-07. Confirmed against the Open WebUI docs: features/chat-conversations/rag (File Context vs Builtin Tools section). Nothing removed.
Method: documentation only; no commands were run.
