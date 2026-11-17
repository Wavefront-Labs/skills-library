---
id: computing-software.systems-network-administration.varnish-cache.request-processing-states
name: request-processing-states
category: computing-software
field: systems-network-administration
product: varnish-cache
tags: [vcl-states, vcl-return-actions, client-side-flow, vcl-step]
level: practitioner
status: docs-checked
description: "Follow a client request through vcl_recv, hash, hit, miss, pass, pipe, purge, deliver and synth, and know which return actions each subroutine allows."
sources:
  - https://www.varnish.org/docs/reference/vcl-step/
  - https://www.varnish.org/docs/reference/states/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# request processing states

Client side:

- `vcl_recv`: decide how to serve. Returns `hash`, `pass`, `pipe`, `purge`, `synth(status, reason)`, `restart`, `vcl(label)` or `fail(err)`.
- `vcl_hash` returns `lookup`: a hit goes to `vcl_hit`, a miss or hit-for-miss to `vcl_miss`, a hit-for-pass to `vcl_pass`; a purge goes to `vcl_purge`.
- `vcl_hit`: `deliver` (a stale object triggers a background refresh), `pass`, `restart`, `synth`.
- `vcl_miss`: `fetch`, `pass`, `restart`, `synth`.
- `vcl_pass`: `fetch`, `restart`, `synth`.
- `vcl_pipe`: `pipe`; Varnish becomes a TCP proxy and no further subs run.
- `vcl_purge`: `restart` or `synth`.
- `vcl_deliver`: `deliver`, `restart`, `synth`.
- `vcl_synth`: `deliver` (skips vcl_deliver) or `restart`; never enters the cache.

`restart` bumps `req.restarts`; past `max_restarts` (default 4) you get a 503. `fail(err)` behaves like synth 503 with request changes rolled back and the connection closed.

`vcl_init` and `vcl_fini` run on load and discard and return `ok` or `fail`.

## Checked

2026-11-04. Compared against the Varnish documentation pages listed in sources (varnishd parameter reference, VCL reference, CLI reference, tutorials and users guide). Removed or corrected: nothing needed removing.

Method: documentation only; no commands were run.
