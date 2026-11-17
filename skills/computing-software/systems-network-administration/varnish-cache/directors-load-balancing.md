---
id: computing-software.systems-network-administration.varnish-cache.directors-load-balancing
name: directors-load-balancing
category: computing-software
field: systems-network-administration
product: varnish-cache
tags: [directors, round-robin, fallback-director, hash-director, shard-director]
level: practitioner
status: docs-checked
description: "Load-balance backends with vmod_directors: round_robin, random with weights, fallback (optionally sticky), hash and shard directors, created in vcl_init."
sources:
  - https://www.varnish.org/docs/reference/vmod_directors/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# directors load balancing

Import `directors`, declare backends, then create directors and add backends in executed VCL; `vcl_init` reproduces the old Varnish 3.0 behaviour. Pick a backend with `.backend()`. Directors can use other directors as backends, and backends can also be added elsewhere in VCL (for example when a certain URL is called).

```vcl
import directors;
sub vcl_init {
    new vdir = directors.round_robin();
    vdir.add_backend(backend1);
    vdir.add_backend(backend2);
}
sub vcl_recv { set req.backend_hint = vdir.backend(); }
```

- `directors.round_robin()`: picks backends in round-robin fashion.
- `directors.random()`: weighted random; `add_backend(be, weight)` gives each backend about `100 * weight / sum(weights)` per cent of traffic (10.0 and 5.0 gives 2/3 and 1/3). Not cryptographic; uses the testable random generator.
- `directors.fallback(sticky=false)`: tries backends in the order added and returns the first healthy one, so add order matters. With `sticky=true` it keeps the chosen healthy backend even when a higher-priority one recovers; once the list is exhausted it starts over.
- `directors.hash()`: `backend(STRING)` hashes the string given; commonly `client.ip` or a session cookie for sticky sessions. `add_backend(be, weight=1.0)`, where 1.0 is the recommended default.
- `directors.shard()`: selects backends by a key (consistent hashing), so the same key gets the same backend unless configuration or health changes; unhealthy backends are not selected by default. Unlike hash it keeps key-to-backend associations as stable as possible when backends change, and offers `set_rampup()` and `set_warmup()`. Key via `backend(by=HASH|URL|KEY|BLOB)`; `by=HASH` is the default. `reconfigure(replicas=67)` runs implicitly at the end of the task if not called. Use `alt=req.restarts` or `alt=bereq.retries` with `healthy=ALL` to pick another server on retries. Check config errors with `varnishlog -I Error:^vmod_directors.shard`.
- Shard drawbacks: distribution depends on requests per key and uniformity of key values, so load balancing can be worse for specific cases; used for persistence it switches back to the preferred server once healthy again.
- `remove_backend(be)` removes a backend; `directors.lookup(STRING)` finds a backend by name (housekeeping context only).

## Checked
2026-11-08. Read in full: the vmod_directors reference page. Confirmed: constructors, methods, weights formula, fallback semantics, hash and shard descriptions. The Users Guide backends page was not read and is dropped. Removed: the claims that unhealthy backends are skipped by every director and that probes are needed (the page states health handling only for fallback and shard), and the `.backend().resolve()` and "resolves at fetch time" statements, which are not on the page.
Method: documentation only; no commands were run.
