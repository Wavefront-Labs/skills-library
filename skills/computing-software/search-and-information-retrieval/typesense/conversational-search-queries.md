---
id: computing-software.search-and-information-retrieval.typesense.conversational-search-queries
name: conversational-search-queries
category: computing-software
field: search-and-information-retrieval
product: typesense
tags: [conversation-search, conversation-model-id, exclude-fields, typesense]
level: advanced
status: docs-checked
description: "Ask questions with Typesense conversational search via multi_search with conversation, conversation_model_id and an auto-embedding query_by."
sources: ["https://typesense.org/docs/30.2/api/conversational-search-rag.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Conversational search queries

Use the search endpoint with these parameters: `conversation=true`, `conversation_model_id=<id>`, `q=<question>` and `query_by=<an auto-embedding field>`.

Example: `POST /multi_search?q=can+you+suggest+an+action+series&conversation=true&conversation_model_id=conv-model-1` with body `{"searches": [{"collection": "tv_shows", "query_by": "embedding", "exclude_fields": "embedding"}]}`.

## Important

Always exclude the embedding field with `exclude_fields`, otherwise the raw floats are passed to the LLM and eat the context window; exclude any other fields irrelevant to answering too.

## Response

A new `conversation` object: show `conversation.answer` to the user; it also has `conversation_history` (with `id`, `last_updated`, `ttl`), `conversation_id` and `query`. Set `exclude_fields: conversation_history` to drop the history from the response.

## multi_search rules

Put `q` in the query string, not in an individual search body. Several collections can be searched; Typesense takes top results from each, and several searches with `conversation=true` still return one conversation object with a single answer.

## Embedding choice

Q&A models such as the `ts/all-MiniLM-L12-v2` S-BERT model work well for conversations; OpenAI embedding models also work.

## Checked

2026-11-09. Confirmed claim by claim against the Typesense documentation page Conversational Search (RAG) (names, defaults, parameters and behaviours as stated in the skill). Removed: nothing; every concrete claim was found on the page.

Method: documentation only; no commands were run.
