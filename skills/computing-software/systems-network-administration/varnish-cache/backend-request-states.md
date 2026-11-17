---
id: computing-software.systems-network-administration.varnish-cache.backend-request-states
name: backend-request-states
category: computing-software
field: systems-network-administration
product: varnish-cache
tags: [vcl-backend-fetch, backend-response, retry-abandon, backend-error]
level: practitioner
status: docs-checked
description: "Control the backend side of VCL: vcl_backend_fetch, vcl_backend_response, vcl_backend_error and vcl_backend_refresh, with retry, abandon, error and max_retries."
sources:
  - https://www.varnish.org/docs/reference/vcl-step/
  - https://www.varnish.org/docs/users-guide/vcl-built-in-code/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# backend request states

- `vcl_backend_fetch`: alter `bereq` before it is sent. Returns `fetch`, `abandon` or `error(status, reason)`. Core code first sets `bereq.method` to GET (unless pass), adds `Accept-Encoding: gzip` when `http_gzip_support` is on, builds conditional headers from a stale object, and sets `bereq.http.X-Varnish`.
- `vcl_backend_response`: runs after headers arrive. Returns `deliver`, `retry`, `abandon`, `pass(duration)` (hit-for-pass) or `error`. Set `beresp.ttl`, `grace`, `keep`, `do_gzip`, `do_esi` here; a stored object cannot change later.
- `vcl_backend_refresh`: after a legitimate 304; returns `merge` (default), `obj_stale`, `beresp`, `retry`, `abandon`, `error`.
- `vcl_backend_error`: on failure or after `max_retries` (default 4). Returning `deliver` with `beresp.uncacheable == false` caches a synthetic object, so set `beresp.uncacheable = true` for private content. `retry` past the limit ends in a 503 via `vcl_synth`.

To cache non-GET requests, save `req.method` in `vcl_recv` and restore it into `bereq.method` here.

A HEAD request can be satisfied from a cached GET response.

## Checked

2026-11-04. Compared against the Varnish documentation pages listed in sources (varnishd parameter reference, VCL reference, CLI reference, tutorials and users guide). Removed or corrected: nothing needed removing.

Method: documentation only; no commands were run.
