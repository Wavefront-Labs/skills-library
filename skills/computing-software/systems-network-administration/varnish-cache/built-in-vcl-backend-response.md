---
id: computing-software.systems-network-administration.varnish-cache.built-in-vcl-backend-response
name: built-in-vcl-backend-response
category: computing-software
field: systems-network-administration
product: varnish-cache
tags: [builtin-vcl, vcl-backend-response, uncacheable-responses, set-cookie]
level: advanced
status: docs-checked
description: "Why responses stay uncacheable by default: ttl <= 0, Set-Cookie, Surrogate-Control no-store, Cache-Control no-cache/no-store/private and Vary: * create hit-for-miss."
sources:
  - https://www.varnish.org/docs/tutorials/varnish-builtin-vcl/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# built in vcl backend response

Built-in `vcl_backend_response`:

```vcl
sub vcl_backend_response {
    if (bereq.uncacheable) {
        return (deliver);
    } else if (beresp.ttl <= 0s ||
      beresp.http.Set-Cookie ||
      beresp.http.Surrogate-control ~ "(?i)no-store" ||
      (!beresp.http.Surrogate-Control &&
        beresp.http.Cache-Control ~ "(?i:no-cache|no-store|private)") ||
      beresp.http.Vary == "*") {
        # Mark as "Hit-For-Miss" for the next 2 minutes
        set beresp.ttl = 120s;
        set beresp.uncacheable = true;
    }
    return (deliver);
}
```

- If `bereq.uncacheable` is set (a pass happened or the object is already hit-for-miss), the response is delivered at once without evaluating cacheability.
- Each trigger creates a hit-for-miss object for 2 minutes, so the next request skips the waiting list (avoiding serialisation) and goes straight to the origin. After that cacheability is re-evaluated; the object is also replaced when a later backend response is cacheable.
- Never set `beresp.ttl` to zero: the hit-for-miss information is lost, the next request can end up on the waiting list and serialisation may occur.

Triggers:
- TTL zero or less: `Cache-Control: max-age=0`, `s-maxage=0`, or an `Expires` in the past.
- `Set-Cookie`: it implies a state change, and caching it would hand the cookie to every user.
- `Surrogate-Control` containing no-store.
- With no Surrogate-Control header, `Cache-Control` containing no-cache, no-store or private. max-age and s-maxage still decide the TTL, and a zero TTL is already uncacheable.
- `Vary: *`. Other Vary values (for example Accept-Language) make a cache variation per request-header value.

If none match, the response is cacheable and is stored with the default TTL or the one from Cache-Control or Expires. The same page notes `vcl_backend_fetch` unsets `bereq.body` for GET.

## Checked

Method: 2026-11-08, read the built-in VCL tutorial in full (docs only, nothing run). Removed the unsupported `vcl_beresp_stale` multi-tier snippet and the unread users-guide/vcl-built-in-code source. Added the bereq.uncacheable shortcut and the per-trigger explanations from the tutorial.
