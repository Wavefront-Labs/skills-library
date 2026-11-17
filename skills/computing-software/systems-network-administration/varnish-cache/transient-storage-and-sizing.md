---
id: computing-software.systems-network-administration.varnish-cache.transient-storage-and-sizing
name: transient-storage-and-sizing
category: computing-software
field: systems-network-administration
product: varnish-cache
tags: [transient, beresp-storage, cache-sizing, shortlived]
level: practitioner
status: docs-checked
description: "Understand Transient storage for short-lived and uncacheable objects, choose a store in VCL with beresp.storage, and size the cache by watching n_lru_nuked."
sources:
  - https://www.varnish.org/docs/users-guide/storage-backends/
  - https://www.varnish.org/docs/users-guide/sizing-your-cache/
  - https://www.varnish.org/docs/reference/varnishd/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# transient storage and sizing

A storage named `Transient` holds short-lived and passed objects; it is the default storage for uncacheable objects from a pass, hit-for-miss or hit-for-pass, and for temporary objects from synthetic responses. If no Transient storage is defined, the default is an unbounded `-s Transient=default`. Other objects rotate between all non-transient stores unless VCL sets `beresp.storage`.

- Short-lived: the `shortlived` parameter (default 10s); objects whose ttl+grace+keep is shorter are always put in transient storage.
- Built-in storage caches full objects only: n concurrent hits on 1GB objects need at least n GB; for uncacheable objects the rule of thumb is n x `transit_buffer`.
- `transit_buffer` (default 0b, meaning no limit) is how many bytes are read from the backend ahead of the client for uncacheable streaming fetches; non-zero values stop large uncacheable objects being stored in full for slow clients, at the cost of holding the backend connection until delivery ends. It defaults `beresp.transit_buffer`.

Naming a store lets VCL pick it:

```bash
varnishd -s fast=malloc,5G -s bulk=file,/path/to/dir,100G ...
```
```vcl
sub vcl_backend_response {
    if (beresp.http.content-type ~ "video") { set beresp.storage = storage.bulk; }
}
```

(The `-s name=` plus `storage.<name>` mechanism is from the varnishd reference; the content-type rule is only an illustration.) Unnamed stores are called s0, s1 and so on.

Sizing (from the sizing guide): consider how big the hot data set is (for a news site, the front page and everything linked from it) and how expensive objects are to regenerate. Watch `n_lru_nuked` with varnishstat; lots of LRU activity means objects are being evicted for space, so consider a bigger cache. `nuke_limit` (default 50) is the maximum number of objects tried for nuking to make room for one object body.

## Checked

Method: 2026-11-08 docs-only read of the storage-backends and sizing pages; the -s, shortlived, nuke_limit and transit_buffer entries in the varnishd reference were checked by search. Removed the earlier `varnishstat -1 -f 'SMA.*'` verify step (not on the pages) and the claim that hit-for-miss and synthetic objects are stored there, which the pages tie to uncacheable and synthetic objects only loosely; wording now follows the pages.
