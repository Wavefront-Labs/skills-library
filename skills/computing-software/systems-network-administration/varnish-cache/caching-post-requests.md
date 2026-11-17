---
id: computing-software.systems-network-administration.varnish-cache.caching-post-requests
name: caching-post-requests
category: computing-software
field: systems-network-administration
product: varnish-cache
tags: [post-caching, cache-req-body, bodyaccess, bereq-method]
level: advanced
status: docs-checked
description: "Cache selected POST requests by hashing the body: std.cache_req_body, bodyaccess hash_req_body, vcl_hash changes and restoring the method in vcl_backend_fetch."
sources:
  - https://www.varnish.org/docs/tutorials/caching-post-requests-varnish/
  - https://www.varnish.org/docs/reference/vmod_std/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# caching post requests

Varnish passes POST by default. To cache chosen POSTs, make the body part of the hash. The tutorial uses `std` and `bodyaccess` (bodyaccess is available as of Varnish 9).

```vcl
import std;
import bodyaccess;

sub vcl_recv {
    unset req.http.X-Body-Len;
    if (req.method == "POST" && req.url ~ "search.html$") {
        if (std.integer(req.http.content-length, 0) > 500000) {
            return (synth(413, "The request body size exceeds the limit"));
        }
        if (!std.cache_req_body(500KB)) { return (hash); }
        set req.http.X-Body-Len = bodyaccess.len_req_body();
        return (hash);
    }
}
sub vcl_hash {
    if (req.http.X-Body-Len) { bodyaccess.hash_req_body(); }
    else { hash_data(""); }
}
```

No `return (lookup)` in `vcl_hash`, so URL and host are still hashed. Varnish changes the method to GET before `vcl_backend_fetch`; restore POST there (for example from a saved header) so the backend sees a POST.

## Checked

2026-11-04. Compared against the Varnish documentation pages listed in sources (varnishd parameter reference, VCL reference, CLI reference, tutorials and users guide). Removed or corrected: the generic closing tip.

Method: documentation only; no commands were run.
