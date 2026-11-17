---
id: computing-software.database-administration.memcached.proxy-settings-limits-timeouts
name: proxy-settings-limits-timeouts
category: computing-software
field: database-administration
product: memcached
tags: [proxy-settings, backend-timeouts, active-req-limit, backend-depth-limit, flapping]
level: sme
status: docs-checked
description: "Proxy settings reference: fast-fail limits, backend timeouts, failure limits and flap backoff with defaults."
sources:
  - https://docs.memcached.org/features/proxy/settings-reference/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Set inside `settings{}`:
- `active_req_limit` 0: fast-fail when more requests in flight than this (0 = none).
- `buffer_memory_limit` 0: fast-fail when about this many KB of value buffers are in use.
- `backend_depth_limit` 0: max queued requests per backend; keep lower than `active_req_limit`.
- `backend_connect_timeout` 5 (s, float); `backend_read_timeout` 3 (s); `backend_retry_waittime` 3 (s).
- `backend_failure_limit` 3: consecutive failures before a backend is marked bad.
- `backend_flap_time` 0: seconds a connection must stay error-free, else it is flapping (0 = never).
- `backend_flap_backoff_ramp` 1.5 and `backend_flap_backoff_max` 3600: retry delay = ramp x retry_waittime x flap count, capped.
- `backend_use_tls` false (needs a build with `--enable-proxy-tls`).
- `backend_use_iothread` false: false scales better but opens more sockets.
- `tcp_keepalive` false.

## Checked

2026-11-04. Confirmed against the Proxy settings reference page (every setting, default and description). Removed: the closing Verify tip.

Method: documentation only; no commands were run.
