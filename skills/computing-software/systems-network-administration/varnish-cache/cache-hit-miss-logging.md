---
id: computing-software.systems-network-administration.varnish-cache.cache-hit-miss-logging
name: cache-hit-miss-logging
category: computing-software
field: systems-network-administration
product: varnish-cache
tags: [x-cache-header, hit-miss-logging, graced-hit, varnishncsa-format]
level: practitioner
status: docs-checked
description: "Record whether each request was a hit, graced hit, miss, pass or synth in an x-cache request header, then read it from the response, varnishlog or varnishncsa."
sources:
  - https://www.varnish.org/docs/tutorials/logging-cache-hits-misses-varnish/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# cache hit miss logging

VCL records the outcome in `req.http.x-cache` in each state:

```vcl
sub vcl_recv { unset req.http.x-cache; }
sub vcl_hit {
    set req.http.x-cache = "hit";
    if (obj.ttl <= 0s && obj.grace > 0s) { set req.http.x-cache = "hit graced"; }
}
sub vcl_miss { set req.http.x-cache = "miss"; }
sub vcl_pass { set req.http.x-cache = "pass"; }
sub vcl_pipe { set req.http.x-cache = "pipe uncacheable"; }
sub vcl_synth { set req.http.x-cache = "synth synth"; }
sub vcl_deliver {
    if (obj.uncacheable) { set req.http.x-cache = req.http.x-cache + " uncacheable"; }
    else { set req.http.x-cache = req.http.x-cache + " cached"; }
}
```

First word: `hit`, `hit graced` (TTL elapsed but still in grace, served while a refreshed object is fetched), `miss`, `pass` (backend fetch that bypassed the cache), `synth`. Second word: `cached` (will be reused), `uncacheable` (from the backend, will not be reused), or `synth`.

Install: paste the snippet at the top of the VCL after the `vcl 4.x;` line, or save it as a file (the tutorial uses /etc/varnish/hit-miss.vcl) and `include "hit-miss.vcl";` after `vcl 4.0;` and `import std;`.

Using it:

- Client: uncomment `set resp.http.x-cache = req.http.x-cache;` in `vcl_deliver` (and in `vcl_synth`). It is off by default because the output may need hiding from regular users. Check with `curl -i`; a response shows e.g. `x-cache: miss cached`. Piped responses cannot be modified, so they never show the header.
- varnishncsa: `varnishncsa -F '<%{x-cache}i> %U %s'`.
- varnishlog: filter with VSL queries, e.g. `varnishlog -q 'ReqHeader:x-cache[1] eq pass'` or `-q 'ReqHeader:x-cache[2] eq cached'`. The same `-q` works with varnishncsa.

## Checked

Method: 2026-11-08 docs-only read of the cited tutorial. VCL, word meanings, install and usage match the page. Removed the earlier "VCL_Log" varnishncsa claim, which the page does not state; replaced with the page's `%{x-cache}i` example.
