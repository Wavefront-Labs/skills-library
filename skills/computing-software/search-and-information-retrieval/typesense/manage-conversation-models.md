---
id: computing-software.search-and-information-retrieval.typesense.manage-conversation-models
name: manage-conversation-models
category: computing-software
field: search-and-information-retrieval
product: typesense
tags: [conversation-models-api, conversation-ttl, model-update, typesense]
level: practitioner
status: docs-checked
description: "List, fetch, update and delete Typesense conversation models via /conversations/models; 24-hour history retention and 409 id conflict."
sources: ["https://typesense.org/docs/30.2/api/conversational-search-rag.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Manage conversations and models

## History retention

Every question and answer is stored in the collection named by `history_collection`, each conversation with a `conversation_id`. Messages persist for 24 hours by default to support follow-ups; change that with the model's `ttl`. Because history is not tied to a search collection, it works with any collection, and the normal collection APIs can manage the messages.

## Model endpoints

- `GET /conversations/models` lists all.
- `GET /conversations/models/<id>` returns one.
- `PUT /conversations/models/<id>` updates it by sending the parameters (for example a changed `system_prompt`, plus `model_name`, `history_collection`, `api_key`, `max_bytes`).
- `DELETE /conversations/models/<id>` removes it.

The `id` itself can be updated; if the new id exists, the API returns `409`. Every call needs the `X-TYPESENSE-API-KEY` header.

## Checked

2026-11-09. Confirmed claim by claim against the Typesense documentation page Conversational Search (RAG) (names, defaults, parameters and behaviours as stated in the skill). Removed: nothing; every concrete claim was found on the page.

Method: documentation only; no commands were run.
