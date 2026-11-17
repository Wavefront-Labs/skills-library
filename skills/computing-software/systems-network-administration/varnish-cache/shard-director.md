---
id: computing-software.systems-network-administration.varnish-cache.shard-director
name: shard-director
category: computing-software
field: systems-network-administration
product: varnish-cache
tags: [shard-director, consistent-hashing, rampup-warmup, varnish-clustering]
level: advanced
status: docs-checked
description: "Use the shard director to pin keys to backends with consistent hashing: key selection, alt for retries, rampup and warmup, and why it helps cache clusters."
sources:
  - https://www.varnish.org/docs/reference/vmod_directors/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# shard director

The shard director picks a backend by key; the same key always maps to the same backend unless configuration or health changes, and associations stay as stable as possible when they do (unlike the hash director). Unhealthy backends are not selected by default.

Uses: improving origin cache efficiency, persistence for a client or session, and Varnish clustering where each object is cached on one node so effective cache size approaches the sum of all nodes. Drawbacks: uneven load if keys are skewed, and requests return to the preferred backend once healthy again.

```vcl
import directors;
sub vcl_init {
    new shard = directors.shard();
    shard.add_backend(be1);
    shard.add_backend(be2);
    shard.reconfigure();                # optional, default replicas=67
}
sub vcl_recv {
    set req.backend_hint = shard.backend(by=URL);
}
```

`by`: `HASH` (default), `URL`, `KEY` (with `shard.key(STRING)`, a SHA256-based key) or `BLOB`.

- `alt`: pick an alternative, for example `alt=bereq.retries` with `healthy=ALL` on retries.
- `rampup`: slow start after a backend becomes healthy (`set_rampup(duration)`).
- `warmup`: send a fraction of requests to the next alternative to warm it.
- `add_backend(be, ident, rampup, weight)`.

## Checked

2026-11-04. Compared against the Varnish documentation pages listed in sources (varnishd parameter reference, VCL reference, CLI reference, tutorials and users guide). Removed or corrected: nothing needed removing.

Method: documentation only; no commands were run.
