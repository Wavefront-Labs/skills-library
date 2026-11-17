---
id: computing-software.search-and-information-retrieval.typesense.conversation-follow-ups-and-streaming
name: conversation-follow-ups-and-streaming
category: computing-software
field: search-and-information-retrieval
product: typesense
tags: [conversation-id, conversation-stream, standalone-question, typesense]
level: advanced
status: docs-checked
description: "Continue a Typesense conversation with conversation_id, standalone-question rewriting, max_bytes limits, and SSE streaming via conversation_stream."
sources: ["https://typesense.org/docs/30.2/api/conversational-search-rag.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Follow-ups and streaming

## Follow-up questions

Add the `conversation_id` returned by the first answer: `.../multi_search?q=how+about+another+one&conversation=true&conversation_model_id=conv-model-1&conversation_id=<ID>`. Typesense then includes the prior context. Internally, for every follow-up it asks the LLM to rewrite the question as a standalone one using the conversation history (prompt: "Rewrite the follow-up question ... as a standalone question that encompasses all pertinent context"), runs semantic or hybrid search with that rewritten question, and forwards the results to the LLM for the answer.

## Context limits

The whole history is stored, but only recent messages fitting within `max_bytes` (after subtracting the system instructions) are sent when forming the standalone question. For retrieval, only top results whose combined size fits the remaining `max_bytes` accompany the question.

## Streaming

Add `conversation_stream=true` as a query parameter. The reply is a Server-Sent Events stream: lines `data: {"conversation": {"message": "...", "conversation_id": "..."}}` for each chunk, ending with `data: [DONE]`. The final response still includes the full conversation object.

The TypeScript client accepts `streamConfig` with `onChunk`, `onError` and `onComplete`; for multi-search it goes in the common params object.

## Checked

2026-11-09. Confirmed claim by claim against the Typesense documentation page Conversational Search (RAG) (names, defaults, parameters and behaviours as stated in the skill). Removed: nothing; every concrete claim was found on the page.

Method: documentation only; no commands were run.
