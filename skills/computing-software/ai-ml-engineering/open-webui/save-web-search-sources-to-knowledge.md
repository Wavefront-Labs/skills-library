---
id: computing-software.ai-ml-engineering.open-webui.save-web-search-sources-to-knowledge
name: save-web-search-sources-to-knowledge
category: computing-software
field: ai-ml-engineering
product: open-webui
tags: [open-webui, web-search, knowledge, function-action, valves]
level: practitioner
status: docs-checked
description: "Install the Add Web Sources to Knowledge action in Open WebUI to save cited web search URLs into a Knowledge Base, with valves and native-mode limits."
sources:
  - https://docs.openwebui.com/features/chat-conversations/web-search/save-to-knowledge
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Save web search results to a Knowledge Base

Goal: one-click save of the URLs cited in a web-search answer into a Knowledge Base.

## Install
It is a **Function Action** from the Open WebUI Community Hub ("Add Web Sources to Knowledge Action"). In Admin Panel > Functions import or create the function with that code, then enable the action globally or for specific models.

## Use
1. Ask something that triggers web search (DDGS, Google PSE, etc.).
2. When citations appear, click the **folder+** icon in the message toolbar.
3. Enter source numbers: `1,3,5`, `1-3` or `all`.
4. Pick the target Knowledge Base. The action fetches pages with your configured **Web Loader** and adds them.

## Valves (admin defaults)
| Valve | Default |
|---|---|
| `max_urls_per_action` | `10` |
| `enable_duplicate_check` | `True` (skips URLs already in the KB) |
| `default_knowledge_base` | empty (name or ID) |
| `skip_confirmation` | `False` |
| `file_name_prefix` | empty (for example `web_`) |

Users can override default Knowledge Base, skip confirmation and file name prefix in their User Valves. Setting a default KB plus Skip Confirmation gives instant one-click saving.

## Gotchas
- In Native (agentic) tool calling, search hits are not sources: only pages the model opened with `fetch_url` are offered. An answer built from snippets alone leaves nothing to save. Legacy mode lists every retrieved result.
- Saved content quality depends on the Web Loader Engine setting (Admin > Settings > Documents per the docs); for JavaScript-heavy sites consider Firecrawl or Playwright.
- No URLs found: check web search is enabled and returning results.

## Checked
2026-11-07. Confirmed against the Open WebUI docs: features/chat-conversations/web-search/save-to-knowledge (read in full). Nothing removed.
Method: documentation only; no commands were run.
