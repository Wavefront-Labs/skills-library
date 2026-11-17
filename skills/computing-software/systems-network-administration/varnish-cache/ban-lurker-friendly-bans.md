---
id: computing-software.systems-network-administration.varnish-cache.ban-lurker-friendly-bans
name: ban-lurker-friendly-bans
category: computing-software
field: systems-network-administration
product: varnish-cache
tags: [ban-lurker, ban-lurker-sleep, obj-http-bans, ban-accumulation]
level: advanced
status: docs-checked
description: "Keep the ban list small: the ban lurker only tests obj.* expressions, so copy URL and host into object headers and ban on those; tune ban_lurker_sleep and avoid req.*."
sources:
  - https://www.varnish.org/docs/users-guide/purging/
  - https://www.varnish.org/docs/tutorials/ban/
  - https://www.varnish.org/docs/tutorials/cache-invalidation/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# ban lurker friendly bans

The ban lurker is a background thread that walks the cache and evicts objects matching bans, but only bans that test `obj.*` fields: the request is not available to it. Avoid `req.*` in bans for that reason.

Bans older than the oldest object are dropped without evaluation. Many long-lived, rarely hit objects can accumulate bans and cost CPU (`bans` counter in varnishstat).

Lurker-friendly pattern:

```vcl
sub vcl_backend_response {
    set beresp.http.x-url = bereq.url;
    set beresp.http.x-host = bereq.http.host;
}
sub vcl_deliver {
    unset resp.http.x-url;
    unset resp.http.x-host;
}
```

Then ban with `obj.http.x-url ~ ... && obj.http.x-host == ...` instead of `req.url`.

Parameters:
- `ban_lurker_sleep` (default 0.010s): pause after the lurker examines objects; 0 disables the lurker.
- `ban_lurker_age` (default 60s): minimum age of a ban before the lurker acts.
- `ban_any_variant` (0 in newer releases): how many non-matching variants a lookup tests.

Inspect the list with `varnishadm ban.list`.

## Checked

2026-11-04. Compared against the Varnish documentation pages listed in sources (varnishd parameter reference, VCL reference, CLI reference, tutorials and users guide). Removed or corrected: the unsupported claim about req bans lingering.

Method: documentation only; no commands were run.
