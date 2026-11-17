---
id: computing-software.ai-ml-engineering.open-webui.setup-rag-external-vector-db-knowledge-source
name: setup-rag-external-vector-db-knowledge-source
category: computing-software
field: ai-ml-engineering
product: open-webui
tags: [open-webui, rag, external-knowledge, qdrant, milvus, pgvector]
level: advanced
status: docs-checked
description: "Attach an existing Qdrant, Milvus or pgvector database to Open WebUI as an experimental external knowledge source with field mapping and a required live test."
sources:
  - https://docs.openwebui.com/features/chat-conversations/rag
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Add an external vector database as a knowledge source

Goal: let chats query your own vector store without re-ingesting documents. This is experimental and the configuration may change between releases.

## Prerequisites
- Provider is Qdrant, Milvus or pgvector, and its Python client (for example `qdrant-client`, `pymilvus`) must exist in the Open WebUI image.
- Vectors in your database must come from the SAME embedding model and dimensions as Open WebUI's configured RAG embedding model; mismatches give poor or meaningless results.

## Steps (Settings > Admin > Integrations > External Knowledge Sources)
1. Create a connection: Provider, Endpoint (URL), API Key/Token if needed, Database/Table/Collection (depends on provider), Timeout.
2. Map result fields (defaults):
   - Content Field `content`, Title Field `title`, Source Field `source`, URL Field `url`, Document ID Field `document_id`, Page Field `page`, Metadata Field `metadata`, Score Field `score`.
   - Dotted paths work for nested fields, e.g. `payload.text`.
3. Test the query with a sample question. Open WebUI runs live retrieval and shows results; a successful test is required before you can create or save the source.

## Result
The source appears under Workspace > Knowledge like any knowledge base and can be attached to models or chats. At chat time Open WebUI embeds the question with its configured embedding model, searches your database by vector, and feeds the top matches into the prompt. No copy of the documents is stored in Open WebUI.

## Gotchas
- In citations a result title is a clickable link only when its Source Field holds a web address; otherwise it is plain text.
- Mismatched embedding model or dimensions produce poor or meaningless results, so confirm they match before blaming the field mapping.

## Checked
2026-11-07. Confirmed against the Open WebUI docs: features/chat-conversations/rag (external knowledge sources section). Reworded the troubleshooting line to what the page says about mismatched embeddings.
Method: documentation only; no commands were run.
