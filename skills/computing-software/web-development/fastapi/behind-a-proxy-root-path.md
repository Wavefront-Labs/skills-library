---
id: computing-software.web-development.fastapi.behind-a-proxy-root-path
name: behind-a-proxy-root-path
category: computing-software
field: web-development
product: fastapi
tags: [fastapi, proxy, root-path, forwarded-allow-ips, x-forwarded, traefik, openapi-servers]
level: advanced
status: docs-checked
description: "Run FastAPI behind Nginx or Traefik: trust forwarded headers with --forwarded-allow-ips, set --root-path for a stripped prefix, and manage OpenAPI servers."
sources: [https://raw.githubusercontent.com/fastapi/fastapi/master/docs/en/docs/advanced/behind-a-proxy.md]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Behind a proxy

## Forwarded headers
- A proxy sets `X-Forwarded-For`, `X-Forwarded-Proto`, `X-Forwarded-Host` so the app learns the client IP, HTTPS and public host.
- For security the server does not interpret them unless told: `fastapi run --forwarded-allow-ips="..."` lists trusted IPs; `"*"` trusts all and suits a server reachable only by the proxy.
- Without it, a redirect from `/items` to `/items/` could go to `http://localhost:8000/items/` instead of `https://mysuperapp.com/items/`.

## Stripped path prefix
- If the proxy serves the app under e.g. `/api/v1` and strips it before forwarding, start with `fastapi run main.py --forwarded-allow-ips="*" --root-path /api/v1`.
- `root_path` is an ASGI concept (also used for mounted sub-apps); read it from `request.scope["root_path"]`.
- FastAPI adds an OpenAPI `servers` entry with that URL, so the docs UI finds `/api/v1/openapi.json`.
- Setting `root_path` in `FastAPI()` is deprecated (docs say in 0.145.0 and earlier it worked); use the CLI option.
- Without a stripped prefix, the proxy passes the full path and nothing special is needed.

## Servers
- Pass `servers=[{"url": ..., "description": ...}]`; FastAPI puts the `root_path` server first.
- `root_path_in_servers=False` removes it.
- If `servers` is omitted and `root_path` is `/`, `servers` is left out of the schema.
- Sub-applications work with `root_path` automatically.

## Verify
Open the docs through the proxy URL (`/api/v1/docs`); the direct server URL docs fail by design.

## Checked

Read the full advanced/behind-a-proxy.md source page. Confirmed the X-Forwarded-For/Proto/Host headers, --forwarded-allow-ips and the wildcard, the fastapi run --root-path example, root_path in scope, the OpenAPI servers entry, the deprecation of root_path in FastAPI() (0.145.0 and earlier), additional servers ordering, root_path_in_servers=False, the servers-omitted note for root_path of /, and sub-application mounts. No claims removed.

Method: docs-only read of cited pages, 2026-11-08
