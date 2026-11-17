---
id: computing-software.systems-network-administration.pi-hole.api-overview-and-errors
name: api-overview-and-errors
category: computing-software
field: systems-network-administration
product: pi-hole
tags: [pihole-api, http-methods, error-handling]
level: practitioner
status: docs-checked
description: "Use the Pi-hole v6 REST API: self-hosted docs, HTTP method semantics, JSON error shape and status codes."
sources: ["https://docs.pi-hole.net/api/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Pi-hole API overview

The API is REST over JSON (UTF-8). The reference matching your exact version is served by your own Pi-hole at `http://pi.hole/api/docs`; the docs for other branches are also published online (replace the branch name `master` with another branch).

**Methods**

| Method | Meaning |
| --- | --- |
| `GET` | Read |
| `POST` | Create |
| `PATCH` | Update existing |
| `PUT` | Create or replace |
| `DELETE` | Delete |

Example: `GET /api/groups` lists groups, `POST /api/groups` creates one, `PUT /api/groups/abc` updates `abc`.

**Errors** have one shape:

```json
{"error": {"key": "unauthorized", "message": "Unauthorized", "hint": null}}
```

`key` categorises (for example `bad_request`, `database_error`), `message` is human-readable, and `hint` may carry detail such as the failing SQL message.

**Status codes**

| Code | Meaning |
| --- | --- |
| 200 | OK |
| 201 | Item created |
| 204 | Item removed |
| 400 | Bad request |
| 401 | No session for an endpoint requiring one |
| 402 | Request failed: parameters were valid but the request failed |
| 403 | Forbidden |
| 404 | Not found |
| 429 | Too many requests |
| 5xx | Pi-hole side error (rare) |

Most endpoints need authentication; if no password is set, none is required.

**Checklist**

1. Read the local `/api/docs`.
2. Branch on `error.key`, not message text.
3. Handle 401 and 429 gracefully.

## Checked

2026-11-04. Confirmed against the official Pi-hole documentation: Pi-hole API (api). Removed the online per-branch docs URL (the page only says per-branch docs exist and links them; the host serves a script shell that could not be read). Added the 402 status the page lists.
Method: documentation only; no commands were run.
