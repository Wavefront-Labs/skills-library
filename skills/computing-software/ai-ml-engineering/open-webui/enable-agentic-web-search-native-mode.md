---
id: computing-software.ai-ml-engineering.open-webui.enable-agentic-web-search-native-mode
name: enable-agentic-web-search-native-mode
category: computing-software
field: ai-ml-engineering
product: open-webui
tags: [open-webui, web-search, agentic-search, native-function-calling, fetch-url]
level: advanced
status: docs-checked
description: "Turn on agentic web search in Open WebUI so a native tool-calling model uses search_web and fetch_url, and cap fetched page length."
sources:
  - https://docs.openwebui.com/features/chat-conversations/web-search/agentic-search
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Enable agentic web search (Native mode)

Goal: let the model decide when to search and read pages itself, using `search_web` and `fetch_url`, instead of classic RAG injection.

## Differences from traditional RAG
- Traditional: Open WebUI decides to search, fetches all results, chunks them and runs RAG.
- Agentic: model decides; `search_web` returns snippets only (no chunking, no vector DB); `fetch_url` reads a full page into context.

## Steps
1. Settings > Admin > Web Search: configure a search engine (hosted LLM-oriented APIs usually give better results than SearXNG).
2. Settings > Admin > Models > pick the model > enable the **Web Search** capability.
3. Same page, **Default Features**: check **Web Search**. Both the capability AND the default feature (or the per-chat toggle) are needed or `search_web`/`fetch_url` are not injected, even if other builtin tools appear.
4. Advanced Parameters: **Function Calling** must be `Native` (the default unless switched to Legacy). Env alternative for a global default: `DEFAULT_MODEL_PARAMS: '{"function_calling": "native"}'`; there is no `FUNCTION_CALLING_MODE` variable.
5. Use a recent model with reliable tool calling; only very old or small models struggle.

## Behaviour to know
- `search_web`: if the model omits `count`, `WEB_SEARCH_RESULT_COUNT` applies; a model-supplied count is capped at that admin maximum. Search hits are NOT citations.
- `fetch_url`: extracts text via your Web Loader and injects it into context. Cap length with Settings > Admin > Web Search > **Fetch URL Content Length Limit** or `WEB_FETCH_MAX_CONTENT_LENGTH`; longer pages end with `[Content truncated...]`. Default is the whole page.
- Fetched pages are the only web citations in Native mode, named by URL.
- Before reading, Open WebUI checks whether the URL is a page or file using the same `USER_AGENT`, headers and Verify SSL setting as the loader; PDFs go through document extraction, and an extensionless URL such as `arxiv.org/pdf/1706.03762` is typed by the server-reported content type.

## Gotchas
- Disabling the Web Search capability hides the tools even if you toggle search in the chat.
- Legacy mode keeps the old RAG-style search and still cites every retrieved result.

## Checked
2026-11-04. Confirmed against the Open WebUI docs page features/chat-conversations/web-search/agentic-search (read in full): the traditional versus agentic comparison, the admin steps, capability plus Default Features requirement, Native as default function calling mode, the DEFAULT_MODEL_PARAMS alternative and absence of FUNCTION_CALLING_MODE, WEB_SEARCH_RESULT_COUNT behaviour, no citations from search hits, WEB_FETCH_MAX_CONTENT_LENGTH and the truncation marker, and the file and extensionless URL handling. Nothing removed.
Method: documentation only; no commands were run.
