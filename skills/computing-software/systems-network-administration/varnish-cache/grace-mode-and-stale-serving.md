---
id: computing-software.systems-network-administration.varnish-cache.grace-mode-and-stale-serving
name: grace-mode-and-stale-serving
category: computing-software
field: systems-network-administration
product: varnish-cache
tags: [grace-mode, request-coalescing, req-grace, keep]
level: advanced
status: docs-checked
description: "Serve stale content safely: request coalescing, grace and keep, what lookup does with expired objects, req.grace with std.healthy, and abandoning 5xx background fetches."
sources:
  - https://www.varnish.org/docs/users-guide/vcl-grace/
  - https://www.varnish.org/docs/tutorials/varnish-builtin-vcl/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# grace mode and stale serving

When several clients request the same page, Varnish sends one backend request and holds the others while it fetches one copy (request coalescing, automatic). At thousands of hits per second the queue can cause a thundering herd, and nobody likes to wait.

Grace: a positive grace tells Varnish to serve the object for some time after its TTL has expired while it fetches a new version. The default comes from the runtime parameter `default_grace`.

Keep: keeps an object in cache for extra time so it can be used to build a conditional GET (If-Modified-Since / If-None-Match) to the backend, which may answer 304 Not Modified and save re-sending the body. Grace and keep are additive: grace 10s plus keep 1m means objects survive 70s after TTL expiry.

```vcl
sub vcl_backend_response {
    set beresp.grace = 2m;
    set beresp.keep = 8m;
}
```

## What lookup does

After `vcl_recv` ends with `return (hash)` and only an object whose TTL has run out is found, Varnish checks whether a backend request is already ongoing and whether the object is within grace:
- Grace run out, no ongoing backend request: `vcl_miss` is called at once and the object is used as a 304 candidate.
- Grace run out, backend request ongoing: the request waits for that fetch.
- Within grace and no backend request: one is scheduled, and `vcl_hit` is called immediately if the object will be delivered. The fetch is asynchronous; when the new object arrives it replaces the old one.

The grace page shows the default `vcl_hit` as `return (deliver);`, while the built-in VCL tutorial shows a version that delivers when `obj.ttl >= 0s`, delivers (with an automatic background fetch) when `obj.ttl + obj.grace > 0s`, and otherwise returns miss. The tutorial also lists three grace sources: the `default_grace` parameter, `beresp.grace` in VCL, and the `stale-while-revalidate` directive in Cache-Control. The grace page notes that in `vcl_hit` the condition `obj.ttl + obj.grace > 0s` always evaluates true; in 6.0.0 and earlier it did not, and the built-in VCL needed a test so that "keep objects" (TTL and grace both gone) were not delivered. Now, when only keep objects exist, `vcl_miss` is called and a fetch starts.

## Misbehaving backends

With health checks enabled you can check whether the backend is sick (`std.healthy`) and change grace:

```vcl
import std;
sub vcl_backend_response {
    set beresp.grace = 24h;
    # no keep - the grace should be enough for 304 candidates
}
sub vcl_recv {
    if (std.healthy(req.backend_hint)) {
        # healthy backend: cap grace to 10s
        set req.grace = 10s;
    }
}
```

`req.grace` limits the effective grace during lookup: with a healthy backend, objects with grace above 10s get an effective 10s; when the backend is sick the default VCL kicks in and the long grace is used.

To stop cache insertion when a background fetch returns a 5xx:

```vcl
sub vcl_backend_response {
    if (beresp.status >= 500 && bereq.is_bgfetch) {
        return (abandon);
    }
}
```

## Checked

Method: 2026-11-08, read the Varnish grace page and built-in VCL tutorial in full (docs only, nothing run). Rewrote to the page's wording: additive grace and keep, the three lookup outcomes, the 6.0.0 vcl_hit note and its req.grace example. Kept the built-in vcl_hit and stale-while-revalidate claims (both are on the built-in VCL tutorial; the grace page's simpler vcl_hit is noted alongside) and replaced "requires probes" with the page's "health checks enabled" wording.
