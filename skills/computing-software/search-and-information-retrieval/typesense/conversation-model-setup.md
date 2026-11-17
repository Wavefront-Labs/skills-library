---
id: computing-software.search-and-information-retrieval.typesense.conversation-model-setup
name: conversation-model-setup
category: computing-software
field: search-and-information-retrieval
product: typesense
tags: [conversational-search, conversation-model, history-collection, typesense]
level: advanced
status: docs-checked
description: "Set up Typesense conversational search: the conversation_store history collection schema and POST /conversations/models for each LLM platform."
sources: ["https://typesense.org/docs/30.2/api/conversational-search-rag.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Conversation model setup

Conversational search answers free-form questions with a built-in RAG pipeline: semantic retrieval from the vector store, then an LLM writes the reply.

## History collection

Create a collection (any name, e.g. `conversation_store`) with exactly this schema, because Typesense fills it automatically: `conversation_id` string, `model_id` string, `timestamp` int32, `role` string with `"index": false`, `message` string with `"index": false`.

## Create the model

`POST /conversations/models` with `id` (optional; one is generated otherwise), `model_name`, `history_collection`, `system_prompt`, `max_bytes` (for example 16384) plus platform fields:

- OpenAI: `model_name` such as `openai/gpt-3.5-turbo`, `api_key`.
- Azure OpenAI: `api_key` and `url` (the Azure OpenAI endpoint URL).
- Google: `api_key`.
- Cloudflare Workers AI: `api_key` and `account_id`.
- vLLM: `vllm_url` (useful for local LLMs).

Other parameters: `ttl` (seconds before messages are deleted, default 86400), `openai_url` and `openai_path` (OpenAI only). Keep `max_bytes` within what the LLM context window supports. The response masks the API key. A sample system prompt restricts answers to the provided context and tells the model to say politely when it has no knowledge.

## Checked

2026-11-09. Confirmed claim by claim against the Typesense documentation page Conversational Search (RAG) (names, defaults, parameters and behaviours as stated in the skill). Removed: the example model_name strings for Azure, Google, Cloudflare and vLLM, which the page does not show in readable form.

Method: documentation only; no commands were run.
