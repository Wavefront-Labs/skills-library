---
id: computing-software.messaging-and-integration.ntfy.server-quick-start
name: server-quick-start
category: computing-software
field: messaging-and-integration
product: ntfy
tags: [ntfy, server, serve, server-yml, environment-variables]
level: intro
status: docs-checked
description: "Start the ntfy server with ntfy serve and configure it from server.yml, flags or NTFY_ environment variables."
sources:
  - https://raw.githubusercontent.com/binwiederhier/ntfy/main/docs/config.md
  - https://raw.githubusercontent.com/binwiederhier/ntfy/main/docs/deprecations.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Running the server

```
ntfy serve
ntfy serve --listen-http :8080
ntfy serve --help
```

With no configuration it listens on port 80 (`Listening on :80`). Running bare `ntfy` no longer starts the server since v1.10.0; use `ntfy serve`.

## Config sources

- Config file, typically `/etc/ntfy/server.yml`
- Command line flags
- Environment variables: prefix `NTFY_`, uppercase with underscores, for example `NTFY_AUTH_DEFAULT_ACCESS`, `NTFY_BASE_URL`. List values are comma-separated.
- In `server.yml` underscores may be used in place of dashes (`cache_duration` and `cache-duration` both work).

Single-quote bcrypt hashes in env vars since they contain `$`.

## Basic keys

```yaml
base-url: "https://ntfy.example.com"
listen-http: ":2586"
cache-file: "/var/cache/ntfy/cache.db"
```

`base-url` is the external URL of the server; it is needed for generated attachment URLs and the e-mail footer. `listen-http` may list several comma-separated addresses.

## Health check

`/v1/health` returns JSON such as `{"healthy":true,"role":"active"}`. A non-200 status or `healthy` set to false means the service is unhealthy.

## Checked

2026-11-04. Confirmed against the ntfy config page (Quick start, config sources, underscores in server.yml, env var rules, base-url, health checks) and deprecations page (bare ntfy replaced by ntfy serve since v1.10.0). Removed: the unstated production wording; Verify replaced by the documented health check.
Method: documentation only; no commands were run.
