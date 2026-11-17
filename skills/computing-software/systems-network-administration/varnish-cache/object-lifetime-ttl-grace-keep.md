---
id: computing-software.systems-network-administration.varnish-cache.object-lifetime-ttl-grace-keep
name: object-lifetime-ttl-grace-keep
category: computing-software
field: systems-network-administration
product: varnish-cache
tags: [ttl, grace, keep, default-ttl]
level: practitioner
status: docs-checked
description: "Set how long objects live: TTL, grace and keep from origin headers, VCL beresp values or parameters, and how they add up to object lifetime."
sources:
  - https://www.varnish.org/docs/tutorials/object-lifetimes/
  - https://www.varnish.org/docs/users-guide/vcl-grace/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# object lifetime ttl grace keep

An object lives for TTL + grace + keep from its origin time. TTL is the fresh window; grace serves stale content while a refresh runs; keep retains the object only to build conditional requests (If-Modified-Since, If-None-Match).

Defaults when the origin sets nothing: `default_ttl` 2m, `default_grace` 10s, `default_keep` 0s.

Precedence: origin headers (`Cache-Control` max-age/s-maxage, `Expires`, `Age`) are honored first, then VCL can change them in `vcl_backend_response`:

```vcl
sub vcl_backend_response {
    set beresp.ttl = 10m;
    set beresp.grace = 2h;
    if (bereq.http.If-Modified-Since) { set beresp.keep = 10m; }
}
```

Change defaults live with `varnishadm param.set default_ttl 1` (lost on restart) or persist `-p default_ttl=1` in the unit file via `systemctl edit --full varnish.service`. `param.reset` restores a default.

Values are additive: grace 10s plus keep 1m survives 70 seconds past TTL. Once cached, an object cannot be modified.

## Checked

2026-11-04. Compared against the Varnish documentation pages listed in sources (varnishd parameter reference, VCL reference, CLI reference, tutorials and users guide). Removed or corrected: nothing needed removing.

Method: documentation only; no commands were run.
