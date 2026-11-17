---
id: computing-software.cloud-infrastructure-engineering.zot.scale-out-ui-sessions
name: scale-out-ui-sessions
category: computing-software
field: cloud-infrastructure-engineering
product: zot
tags: [zot, session-driver, sticky-sessions, redis-sessions, haproxy-cookie, scale-out-ui]
level: advanced
status: docs-checked
description: "Make the Zot web UI and zli work in a scale-out cluster with Redis-compatible session storage (v2.1.9+) or HAProxy sticky cookies on older releases."
sources:
  - https://raw.githubusercontent.com/project-zot/project-zot.github.io/main/docs/articles/scaleout.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The UI and `zli` need all cluster instances to share session information.

From v2.1.9 Zot supports external Redis-compatible session storage under `http.auth.sessionDriver`:

```json
"sessionDriver": { "name": "redis", "url": "redis://localhost:6379", "keyprefix": "zotsession" }
```

The documented UI sample builds on the compute-only Redis sample (shared S3 storage and Redis cache driver) and adds:
- `http.auth.htpasswd.path`
- the `sessionDriver` above
- `extensions.search.enable: true` and `extensions.ui.enable: true`

Older releases: use a load balancer with a sticky session cookie. The HAProxy sample uses a `frontend zot` on `*:8080`, a `backend zot-cluster` in `mode http` with `balance roundrobin`, `cookie SERVER insert indirect nocache`, and one `server` line per instance with `check` and a distinct cookie value.

DNS-based balancing may not suit workloads needing sticky cookies. In the compute-and-storage (local) scale-out variant the UI is not supported at all.

## Checked

2026-11-04. Read against the zot scale-out article (web UI, zli, HAProxy sections); every remaining claim found there. Removed: nothing.

Method: documentation only; no commands were run.
