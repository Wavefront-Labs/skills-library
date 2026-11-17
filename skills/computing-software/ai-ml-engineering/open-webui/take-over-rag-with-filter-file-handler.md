---
id: computing-software.ai-ml-engineering.open-webui.take-over-rag-with-filter-file-handler
name: take-over-rag-with-filter-file-handler
category: computing-software
field: ai-ml-engineering
product: open-webui
tags: [functions-pipe-filter-action, filter, file-handler, rag, redaction, open-webui]
level: advanced
status: docs-checked
description: "Replace Open WebUI built-in retrieval from a Filter with self.file_handler = True to redact, rerank or access-control chunks before they reach the model."
sources:
  - https://docs.openwebui.com/features/extensibility/plugin/functions/filter
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: run your own retrieval and inject chunks yourself.

## Why
At `inlet()` time `body["metadata"]["files"]` and `body["files"]` hold only references (ids, names, types). Built-in RAG runs after every inlet filter and then wraps chunks in `<source>` tags. If you only need to transform what built-in RAG produced, use a `request` filter instead (it sees injected chunks, no opt-in). Use `file_handler` to REPLACE retrieval: custom hybrid scoring, query rewriting, different reranker, chunk-level ACLs, per-model redaction (branch on `__model__["owned_by"]`).

## Enable
```python
class Filter:
    def __init__(self):
        self.valves = self.Valves()
        self.file_handler = True   # instance attribute or class attribute
    async def inlet(self, body, __request__=None, __user__=None, __model__=None):
        ...
        return body
```
A bare module-level `file_handler = True` is silently ignored. After `inlet()` returns, Open WebUI strips `body["metadata"]["files"]` and `body["files"]`, so the built-in RAG is skipped. It applies to `inlet` only; a filter with just `request`/`stream`/`outlet` is unaffected.

## Recipe
1. Read references from `body["metadata"]["files"]` and `body["files"]`.
2. Retrieve: HTTP `POST /api/v1/retrieval/query/doc` (one collection) or `/api/v1/retrieval/query/collection` (several), with the user's last message as the query and the inbound bearer token so permissions stay user-scoped; or in-process `from open_webui.retrieval.utils import get_sources_from_items` (returns dicts with `document` array and parallel `metadata` array).
3. Transform chunks.
4. Inject into `body["messages"]`. For clickable citations mirror:
```html
<source id="1" name="filename.pdf" resource-id="<collection_id>" resource-type="collection">
...chunk text...
</source>
```
Plain Markdown works but loses the citation popovers.
5. Return `body`.

## Gotchas
- The flag is static and read off the cached instance before each `inlet()`; changing it inside `inlet()` applies from the next request. When set, built-in RAG is ALWAYS skipped whenever the filter runs, so you must handle retrieval in every scenario.
- For per-request switching, make the filter user-toggleable (`self.toggle = True`): when not selected it does not run and built-in RAG proceeds.
- Clearing `body["files"]` manually in inlet works today but is brittle; prefer the documented flag.

## Checked
2026-11-07. Confirmed against the Open WebUI docs: features/extensibility/plugin/functions/filter (read in full). Nothing removed.
Method: documentation only; no commands were run.
