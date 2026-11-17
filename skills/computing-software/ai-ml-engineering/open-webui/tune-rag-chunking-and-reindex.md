---
id: computing-software.ai-ml-engineering.open-webui.tune-rag-chunking-and-reindex
name: tune-rag-chunking-and-reindex
category: computing-software
field: ai-ml-engineering
product: open-webui
tags: [open-webui, rag, chunking, embeddings, reindex, markdown-splitting]
level: practitioner
status: docs-checked
description: "Tune Open WebUI RAG chunk size, overlap, splitter and min-size target, and know exactly when a re-index is needed after changing chunking or the embedding model."
sources:
  - https://docs.openwebui.com/features/chat-conversations/rag
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Tune RAG chunking and re-index after changes

Goal: get coherent retrieval chunks and keep the vector store consistent after a settings change.

## Where
Settings > Admin > Documents. The embedding model (Ollama or OpenAI models) is chosen here too.

## Chunking settings
- **Text Splitter** (`RAG_TEXT_SPLITTER`): `character` (default, RecursiveCharacterTextSplitter), `token` (Tiktoken counts) or `token_transformers` (HuggingFace tokenizer named by `RAG_TOKENIZER_MODEL`, e.g. `bert-base-uncased`, matching your embedding model; not available on the slim image).
- **Chunk Size** and **Chunk Overlap**.
- **Markdown Header Splitting**: splits on H1-H6 first, then the normal splitter runs on the pieces.
- **Chunk Min Size Target** (`CHUNK_MIN_SIZE_TARGET`): merges tiny header-split fragments forward into the next chunk. A chunk absorbs the next one only if the accumulated text is still under the target, the merge stays within `CHUNK_SIZE`, and both come from the same source file. Docs example: target 1000 with chunk size 2000 can cut chunk counts by over 90 percent while improving accuracy.

## What a change requires
| Change | New files | Existing knowledge bases | Standalone chat files |
|---|---|---|---|
| Chunk size/overlap | use new values | old chunks still work; re-index recommended for consistency | re-upload |
| Embedding model | use new model | re-index REQUIRED (incompatible vector spaces) | re-upload |

## Re-index
After changing the embedding model, go to Settings > Admin > Documents and click **Reindex**. It deletes each knowledge base's vector collection, re-chunks every file with current settings, re-embeds with the current model, and rebuilds each file's per-file collection.

## Gotchas
- Re-index works from the text extracted at first upload; it does NOT re-parse the original file, so changing the extraction engine has no effect on existing files. Re-upload them.
- Files uploaded straight into a chat (not in a knowledge base) are not touched by re-index.
- Ollama defaults context to 4096 tokens on GPUs under 24 GiB, which starves RAG; raise context length (8192+, ideally over 16000) in Settings > Admin > Models > edit model > Advanced Params.
- To let the model cite page numbers, set `RAG_SOURCE_METADATA_KEYS`.

## Checked
2026-11-07. Confirmed against the Open WebUI docs: features/chat-conversations/rag (chunking and re-index sections). Nothing removed.
Method: documentation only; no commands were run.
