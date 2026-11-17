---
id: computing-software.ai-ml-engineering.open-webui.troubleshoot-web-search-failures
name: troubleshoot-web-search-failures
category: computing-software
field: ai-ml-engineering
product: open-webui
tags: [open-webui, troubleshooting, web-search, proxy, user-agent]
level: practitioner
status: docs-checked
description: "Diagnose Open WebUI web search problems: proxy fetch failures, SearXNG 403, empty page content, models that never call search_web, and timeouts."
sources:
  - https://docs.openwebui.com/troubleshooting/web-search
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Troubleshoot web search

Goal: first separate a failed search request from a failure to read the returned pages, then apply the matching fix.

## 1. Search works behind a proxy but pages fail
Errors: `[Errno -3] Temporary failure in name resolution`, `Connection timeout to host`, `None of the web search results could be loaded`. The page fetcher ignores `http_proxy`/`https_proxy` by default. Enable **Trust Proxy Environment** in Settings > Admin > Web Search, or set `WEB_SEARCH_TRUST_ENV=True`.

## 2. SearXNG `403 Client Error: Forbidden`
JSON output is not enabled. In SearXNG `settings.yml` add `json` under `search: formats:` beside `html`, then restart SearXNG.

## 3. Empty content or poor results
- Context too small: Ollama defaults to 4096 tokens on GPUs under 24 GiB; set 16384+ in Settings > Admin > Models > Edit > Advanced Params.
- Tune `WEB_SEARCH_RESULT_COUNT` (in Native mode it is the default and the cap for the model-supplied `count`).
- Change `WEB_LOADER_ENGINE` to `playwright` for JavaScript-heavy sites or `firecrawl`/`tavily` for extraction.
- Bot blocking (Wikipedia, Cloudflare sites return empty or 403): set `USER_AGENT` to a real browser string; it also covers `fetch_url` and `#` page attachments, including the file-type check for PDFs.
- `The server answered with a compressed response, which is not accepted.`: Open WebUI asks for uncompressed content; re-upload objects (for example S3/MinIO) without a `Content-Encoding` header.

## 4. Model never calls `search_web`
Usually model capability. Use a modern tool-calling model, confirm Function Calling = Native (Settings > Admin > Models > Edit > Advanced Params), and check all three gates: web search enabled globally, enabled on the model, and toggled on in the chat. For DDGS, verify the provider separately; if logs show results but no tool call, switch models.

## 5. Timeouts
Set `WEB_SEARCH_CONCURRENT_REQUESTS=1` (needed for the Brave free tier), lower `WEB_LOADER_CONCURRENT_REQUESTS`, and verify the container can reach both the engine and result URLs.

## Gotcha: where settings live
These are persisted settings: the env var seeds the first value, then the saved Admin Panel value wins and applies to the next search without a restart. Check the admin panel first. Loader settings save without an engine; while Web Search is off, search-only settings are hidden but kept.

## Checked
2026-11-07. Confirmed against the Open WebUI docs: troubleshooting/web-search (read in full). Nothing removed.
Method: documentation only; no commands were run.
