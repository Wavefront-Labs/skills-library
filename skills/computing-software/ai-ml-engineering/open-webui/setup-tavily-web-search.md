---
id: computing-software.ai-ml-engineering.open-webui.setup-tavily-web-search
name: setup-tavily-web-search
category: computing-software
field: ai-ml-engineering
product: open-webui
tags: [open-webui, web-search, tavily, web-loader, search-confirmation]
level: practitioner
status: docs-checked
description: "Enable Tavily as the Open WebUI web search engine, set its search depth and base URL, and understand the search engine versus web loader split and confirmation prompt."
sources:
  - https://docs.openwebui.com/features/chat-conversations/web-search
  - https://docs.openwebui.com/features/chat-conversations/web-search/providers/tavily
  - https://docs.openwebui.com/troubleshooting/web-search
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Configure Tavily as the web search engine

Goal: real-time web search through Tavily's AI-oriented search API (community guide).

## Concept first
Web search is two jobs: the **Web Search Engine** finds links with previews; the **Web Loader Engine** reads the page text behind a link. Choose one engine and leave the loader on its default to start. Tavily (and Exa) can do both jobs, so they appear in both lists. Loader settings still apply with web search off; the engine is only required while Web Search is on.

## Steps
1. Create an API key at the Tavily dashboard (check plan query limits).
2. Admin account: Admin Panel > Settings > Web Search. Toggle **Web Search** on, choose **tavily** in Web Search Engine, paste the **Tavily API Key**.
3. Optional env instead of the UI: `-e TAVILY_API_KEY="your_tavily_api_key"`.
4. Save, open a chat, use the Integrations button (the + area) to enable web search, ask something current.

## Tuning
- Open WebUI sends `query`, `max_results` and `search_depth`. **Tavily Search Depth** (`TAVILY_SEARCH_DEPTH`) accepts `ultra-fast`, `fast`, `basic` (default) or `advanced`.
- Requests go to `TAVILY_API_BASE_URL` + `/search` (default `https://api.tavily.com`); this one is env-only, no admin field.
- Domain filtering is not sent to Tavily; Open WebUI's own **Domain Filter List** is applied after results return.

## Require confirmation
Admins can make users confirm before a search runs: Settings > Admin > Web Search switch, or `ENABLE_WEB_SEARCH_CONFIRMATION`; prompt text via `WEB_SEARCH_CONFIRMATION_CONTENT`.

## Gotchas
- Invalid key: re-copy without spaces. No results: confirm the per-chat web search toggle is on. Settings not saved: need admin and a writable `webui.db`.
- Results found but page content empty: that is a page-reading problem, not a search problem. The web search troubleshooting guide covers `WEB_LOADER_ENGINE` and `USER_AGENT`.

## Checked
2026-11-07. Confirmed against the Open WebUI docs: features/chat-conversations/web-search index and providers/tavily. Added the web search troubleshooting page to sources and reworded the empty-content gotcha to what that page says.
Method: documentation only; no commands were run.
