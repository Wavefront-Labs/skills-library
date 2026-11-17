---
id: computing-software.systems-network-administration.incus.rest-api-basics
name: rest-api-basics
category: computing-software
field: systems-network-administration
product: incus
tags: [incus, rest-api, async-operations, status-codes, recursion, filter, etag, incus-query]
level: practitioner
status: docs-checked
description: "Use the Incus REST API: sync, async and error responses, status codes, recursion and OData-style filter, ETag with If-Match, PUT vs PATCH, and incus query/--debug."
sources:
  - https://raw.githubusercontent.com/lxc/incus/main/doc/rest-api.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# REST API basics

- `GET /` lists supported major versions; non-breaking additions appear in `api_extensions`.
- Sync: HTTP 200, `type` "sync", `status_code` 200. Async: HTTP 202 with a `Location` header to the operation; `type` "async", `status_code` 100; operation fields include `id`, `class` (task, websocket, token), `status`, `resources`, `may_cancel`, `err`. Error: `type` "error", HTTP 400/401/403/404/409/412/500.
- Rely on numeric `status_code`: 100-199 state (e.g. 103 Running, 110 Frozen), 200 Success, 400 Failure, 401 Canceled.
- `recursion=0` (default) returns URLs; `recursion=1` returns the objects.
- `filter=field eq value` with `not`, `eq`, `ne`, `and`, `or` (left to right, quote values with spaces, nesting allowed); config via `config.key`, devices via `devices.name.field`.
- Concurrency: send the `ETag` from GET as `If-Match` on PUT. PUT replaces the whole object, PATCH only given fields.
- Operations over about one second run in the background; subscribe to notifications before starting remote operations.
- Tools: `incus query <path>`; any `incus` command with `--debug` shows API calls.

## Checked

2026-11-09. Confirmed against the Incus REST API page: versioning and api_extensions, sync/async/error shapes and HTTP codes, operation fields and classes, status code ranges and values, recursion, filter language and examples, one-second background rule, notifications, ETag/If-Match, PUT vs PATCH, incus query and --debug. Nothing removed.
Method: documentation only; no commands were run.
