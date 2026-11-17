---
id: computing-software.systems-network-administration.paperless-ngx.ai-features-setup
name: ai-features-setup
category: computing-software
field: systems-network-administration
product: paperless-ngx
tags: [paperless-ngx, ai, llm, ollama, llm-index, document-chat]
level: advanced
status: docs-checked
description: "Enable optional LLM suggestions, similar documents and chat with Ollama or an OpenAI-compatible API, and maintain the LLM index."
sources:
  - "https://docs.paperless-ngx.com/advanced_usage/"
  - "https://docs.paperless-ngx.com/administration/"
  - "https://docs.paperless-ngx.com/usage/"
  - "https://docs.paperless-ngx.com/faq/"
  - "https://docs.paperless-ngx.com/configuration/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AI features

Off by default and never a replacement for the built-in classifier suggestions. Enabling sends document content and metadata to your LLM backend; with a remote provider your documents leave your server and may incur charges. Prefer a local backend if that matters.

## Minimum settings
- `PAPERLESS_AI_ENABLED=true`
- `PAPERLESS_AI_LLM_BACKEND`: `ollama` or `openai-like`
- `PAPERLESS_AI_LLM_MODEL`
- `PAPERLESS_AI_LLM_ENDPOINT` (required for Ollama) and, for openai-like, usually `PAPERLESS_AI_LLM_API_KEY`
All can also be set under Settings > Application Configuration; the database value wins over the environment.

## Suggestions
The Suggest button on the document page proposes title, tags, correspondent, type, storage path and dates. Choose ML, AI or both under Settings > Documents. `PAPERLESS_AI_LLM_OUTPUT_LANGUAGE` sets the language.

## LLM index and chat
Set `PAPERLESS_AI_LLM_EMBEDDING_BACKEND` (`huggingface` for local, `ollama`, `openai-like`). It builds a vector index for retrieval, similar documents and chat. Huggingface downloads its model on first use, so it needs network access and disk space. The index updates on `PAPERLESS_LLM_INDEX_TASK_CRON` (daily). Manage it:
```bash
document_llmindex rebuild
document_llmindex update
document_llmindex compact
```
`rebuild` is for first use or after changing the backend or model. They do nothing unless AI and an embedding backend are configured.

## Security
Content is passed as untrusted data. `PAPERLESS_AI_LLM_ALLOW_INTERNAL_ENDPOINTS=false` blocks private and loopback endpoints.

## Checked
2026-11-04. Read the AI features section of advanced_usage, the LLM index section of administration, and the AI section of configuration (Markdown source of the Paperless-ngx docs; the rendered site blocks scripts). Confirmed: off by default, minimum settings, Ollama endpoint requirement, database value over environment, Suggest button and ML/AI/both choice, output language setting, embedding backends, huggingface first-use download, daily index cron, document_llmindex rebuild/update/compact and the no-effect note, internal endpoint setting. Nothing removed.

Method: documentation only; no commands were run.
