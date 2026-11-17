---
id: computing-software.ai-ml-engineering.open-webui.setup-searxng-web-search
name: setup-searxng-web-search
category: computing-software
field: ai-ml-engineering
product: open-webui
tags: [open-webui, web-search, searxng, docker]
level: practitioner
status: docs-checked
description: "Self-host SearXNG with JSON output enabled and point Open WebUI web search at it, including env vars, connectivity check and the 403 fix."
sources:
  - https://docs.openwebui.com/features/chat-conversations/web-search/providers/searxng
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Configure SearXNG as the web search engine

Goal: Open WebUI web search served by your own SearXNG (community guide).

## 1. Run SearXNG with JSON enabled
Compose service: image `searxng/searxng:latest`, port `8080:8080`, volume `./searxng:/etc/searxng:rw`, `env_file: .env` containing `SEARXNG_HOSTNAME=localhost:8080/`, `cap_drop: ALL` plus `cap_add` CHOWN, SETGID, SETUID, DAC_OVERRIDE.
- First run: remove `cap_drop: ALL` so SearXNG can create `/etc/searxng/uwsgi.ini`; re-add it afterwards.
- Run about 30 seconds, `docker compose down`, then edit `./searxng/settings.yml`: under `search:` `formats:` add `- json` next to `- html`. Restart with `docker compose up -d`.
- Without JSON, SearXNG blocks queries and Open WebUI logs `403 Client Error: Forbidden`.
- With the searxng-docker repo variant, also create `searxng/limiter.toml` with `[botdetection.ip_limit]` `link_token = false` and empty `block_ip` / `pass_ip` lists under `[botdetection.ip_lists]`.

## 2. Configure Open WebUI
Environment form:
```yaml
ENABLE_WEB_SEARCH: True
WEB_SEARCH_ENGINE: "searxng"
WEB_SEARCH_RESULT_COUNT: 3
WEB_SEARCH_CONCURRENT_REQUESTS: 10
SEARXNG_QUERY_URL: "http://searxng:8080/search"
```
Or Settings > Admin > Web Search: enable, engine `searxng`, Searxng Query URL. Point it at `/search`; Open WebUI adds `q`, `format=json` and `language` itself. `SEARXNG_LANGUAGE` defaults to `all`.

## Verify
`docker exec -it open-webui curl "http://host.docker.internal:8080/search?q=this+is+a+test+query&format=json"`

## Mutual TLS
Set `SEARXNG_CLIENT_CERT_FILE` and optionally `SEARXNG_CLIENT_KEY_FILE`, and mount the certs into the container (for example `-v /path/to/certs:/certs:ro`). The cert is read once, so restart after replacing it.

## Use in chat
Toggle Web Search under the Integrations button next to +. It is per session: reloading or switching chats turns it off.

## Checked
2026-11-07. Confirmed against the Open WebUI docs: features/chat-conversations/web-search/providers/searxng (read in full). Nothing removed.
Method: documentation only; no commands were run.
