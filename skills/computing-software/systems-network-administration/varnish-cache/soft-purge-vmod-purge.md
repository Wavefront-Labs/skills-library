---
id: computing-software.systems-network-administration.varnish-cache.soft-purge-vmod-purge
name: soft-purge-vmod-purge
category: computing-software
field: systems-network-administration
product: varnish-cache
tags: [soft-purge, vmod-purge, purge-hard, purge-grace]
level: advanced
status: docs-checked
description: "Use vmod_purge for finer control than return(purge): purge.hard() and purge.soft(ttl, grace, keep) from vcl_hit and vcl_miss; a soft purge only ever shortens lifetime."
sources:
  - https://www.varnish.org/docs/reference/vmod_purge/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# soft purge vmod purge

vmod_purge functions offer finer control than `return (purge)` from `vcl_recv`. They can only be called from `vcl_hit` and `vcl_miss`, and should generally be used in both so all variants of an object are handled.

```vcl
import purge;
sub vcl_recv {
    if (req.method == "PURGE") {
        if (client.ip !~ purge_acl) { return (synth(405)); }
        return (hash);
    }
}
sub my_purge {
    set req.http.purged = purge.hard();
    if (req.http.purged == "0") { return (synth(404)); }
    else { return (synth(200)); }
}
sub vcl_hit  { if (req.method == "PURGE") { call my_purge; } }
sub vcl_miss { if (req.method == "PURGE") { call my_purge; } }
sub vcl_synth {
    if (req.method == "PURGE") {
        if (req.http.purged) { set resp.http.purged = req.http.purged; }
        return (deliver);
    }
}
```

`purge_acl` is not defined by the page; supply your own ACL.

- `purge.hard()`: equivalent to `return (purge)` but called from `vcl_hit`/`vcl_miss`; returns the number of purged objects.
- `purge.soft(ttl=0, grace=-1, keep=-1)`: sets ttl, grace and keep. A negative grace or keep, or a value higher than the object's current one, leaves it untouched. All three 0 equals a hard purge. Returns the number of soft-purged objects.

A soft purge can only decrease lifetime. Worked cases from the page, for an object with ttl, grace and keep of 60s each:

- `purge.soft(0s, -1s, -1s)`: fresh object gets ttl 0 and expires after 120 seconds; a stale object's expiry is unchanged.
- `purge.soft(0s, 10s, 10s)`: fresh, expires after 20 seconds; stale for 5s, expires after 15 seconds; stale for 15s, after 5 seconds; stale for 20s or more, expires immediately.
- `purge.soft(10s, -1s, -1s)`: fresh for 5s, ttl becomes 10s and it expires after 130 seconds; fresh for 55s, ttl unchanged (125 seconds); stale, unchanged.

Logging: a reduced expiry logs `EXP_Reduce` under the `ExpKill` VSL tag; an unchanged one logs `EXP_Unchanged`.

## Checked

Method: 2026-11-08 docs-only read of the vmod_purge reference. Earlier claims matched the page; added the page's worked expiry examples and ExpKill logging, and noted that purge_acl is not defined by the page.
