---
id: computing-software.systems-network-administration.varnish-cache.http-purge
name: http-purge
category: computing-software
field: systems-network-administration
product: varnish-cache
tags: [purge, purge-acl, return-purge, cache-invalidation]
level: practitioner
status: docs-checked
description: "Invalidate single objects with HTTP PURGE: ACL-protected vcl_recv handler, return(purge), what it removes, and how to trigger it with curl."
sources:
  - https://www.varnish.org/docs/users-guide/purging/
  - https://www.varnish.org/docs/tutorials/purge/
  - https://www.varnish.org/docs/tutorials/cache-invalidation/
  - https://www.varnish.org/docs/tutorials/varnish-builtin-vcl/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# http purge

A purge picks an object out of the cache and discards it along with its Vary variants, immediately. It cannot use regular expressions, and it evicts regardless of backend availability (if the backend is down, there is no copy left to serve). Purging is not in the built-in VCL; you must write it.

```vcl
vcl 4.1;
acl purge { "localhost"; "192.168.55.0"/24; }
sub vcl_recv {
    if (req.method == "PURGE") {
        if (client.ip !~ purge) { return (synth(405, "Method Not Allowed")); }
        return (purge);
    }
}
```

`return (purge)` ends `vcl_recv` and jumps to `vcl_hash`; when that returns lookup, Varnish purges the object and then calls `vcl_purge`, where you can add further actions; the built-in `vcl_purge` is `return (synth(200, "Purged"))`, so the client gets a synthetic 200 Purged response. The request must hash like the cached one: the default `vcl_hash` uses the Host header and the URL including query parameters, so purging is per host and per URL.

Trigger (change the response body by overriding `vcl_synth` and setting `resp.body`):

```bash
curl -X PURGE "http://www.example.com/foo"
# or, for another hostname: send the matching Host header
```

Apply the VCL first (the tutorial reloads with `systemctl reload varnish`).

Notes from the pages:
- Always restrict by ACL; an exposed purge endpoint could tank your hit rate. Keep the ACL up to date.
- The method name is yours to choose, but the VCL must explicitly handle it: otherwise the built-in VCL pipes the request to the backend, and a backend 200 OK does not confirm a purge.
- Alternatives: bans (expression-based), forcing a miss with `req.hash_always_miss` (the old object stays until TTL expiry or eviction), and xkey (tag-based) purging.

## Checked

Method: 2026-11-08, read the four cited Varnish pages in full (docs only, nothing run). The built-in `vcl_purge` claim is confirmed by the built-in VCL tutorial (added as a source); the bans/xkey comparison is stated on the cache-invalidation page. ACL, return(purge) flow and curl usage were unchanged.
