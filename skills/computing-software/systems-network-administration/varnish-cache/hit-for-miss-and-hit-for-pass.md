---
id: computing-software.systems-network-administration.varnish-cache.hit-for-miss-and-hit-for-pass
name: hit-for-miss-and-hit-for-pass
category: computing-software
field: systems-network-administration
product: varnish-cache
tags: [hit-for-miss, hit-for-pass, uncacheable, waiting-list]
level: advanced
status: docs-checked
description: "Choose between pass, hit-for-miss and hit-for-pass for uncacheable content, and how to detect each in the VSL."
sources:
  - https://www.varnish.org/docs/users-guide/increasing-your-hitrate/
  - https://www.varnish.org/docs/tutorials/vsl-cheatsheet/
  - https://www.varnish.org/docs/tutorials/varnish-builtin-vcl/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# hit for miss and hit for pass

On a cache miss Varnish coalesces concurrent fetches: one runs, the rest wait. For content that turns out uncacheable, waiting requests may serialise (each waits for the previous fetch, then the next begins). The three mechanisms below avoid that.

## pass

`return (pass)` in `vcl_recv`, for requests you can recognise as uncacheable (a URL pattern, a header):

```vcl
sub vcl_recv {
  if (req.url ~ "^/this/is/personal/") { return(pass); }
}
```

No request coalescing; `bereq.uncacheable` and `beresp.uncacheable` are both true and the response is never cached even if Cache-Control would allow it. Built-in `vcl_recv` passes non-GET/HEAD methods and requests with Cookie or Authorization. Client If-* headers go to the backend, so the backend can answer 304; Varnish may also send a 304 to the client if the headers allow it (remove the If-* request headers in `vcl_pass` to prevent that).

## hit-for-miss (default)

When a non-passed response is uncacheable, `beresp.uncacheable` is true and a minimal object remembers this for `beresp.ttl` (the built-in VCL uses 120s for TTL 0, Set-Cookie and similar). No coalescing, so fetches run concurrently. A hit-for-miss lookup runs `vcl_miss`. Fetches are like misses: not conditional (If-Modified-Since / If-None-Match removed from the backend request), and the response may become cacheable later. The state ends when the TTL elapses or a cacheable response arrives, which replaces the object. After expiry the next request is an ordinary miss with coalescing. Never set `beresp.ttl` to zero here (hit-for-miss information is lost).

```vcl
sub vcl_backend_response {
  if (beresp.http.X-This-Is == "personal") { set beresp.uncacheable = true; }
}
```

Once true, `beresp.uncacheable` cannot be set back to false (attempts are ignored).

## hit-for-pass

Because hit-for-miss fetches cannot be conditional, large uncacheable responses that the backend could validate with 304 need hit-for-pass: `return(pass(DURATION))` from `vcl_backend_response`.

```vcl
sub vcl_backend_response {
  if (beresp.ttl <= 0s && (beresp.http.ETag || beresp.http.Last-Modified)) {
    return(pass(120s));
  }
}
```

A minimal object marks the state; matching requests are processed as a pass (`vcl_pass` runs), with no coalescing and If-* client headers passed to the backend. Responses are never cached during the window, even if cacheable, so unlike hit-for-miss it cannot end early with a cacheable response. You can end it by setting `req.hash_always_miss` to true in `vcl_recv` for a request that hits the object. After the DURATION the next request is an ordinary miss. Nothing in the built-in VCL uses hit-for-pass; you must add the return yourself.

## Finding them in the VSL

```
varnishlog -q 'Link[3] eq pass'                           # passes
varnishlog -q 'HitMiss'                                   # hit-for-miss requests
varnishlog -q 'TTL[6] eq uncacheable'                     # backend responses marked HfM (also shows HfP insertions)
varnishlog -q 'TTL[6] eq uncacheable and VCL_return eq deliver'  # same without -g, excluding HfP
varnishlog -q 'Link[3] eq pass and VCL_return eq lookup'  # hit-for-pass requests
varnishlog -q 'TTL[1] eq HFP'                             # hit-for-pass insertions
```

## Checked

Method: 2026-11-08, read the increasing-your-hitrate and VSL cheatsheet pages in full and the built-in VCL tutorial (docs only, nothing run). Added the pass details, hit-for-miss lifetime and conditional-fetch rules, the VCL examples and the extra query that separates HfM from HfP. The "waiting list serialises" rationale, uncacheable-is-sticky and hash_always_miss claims were confirmed.
