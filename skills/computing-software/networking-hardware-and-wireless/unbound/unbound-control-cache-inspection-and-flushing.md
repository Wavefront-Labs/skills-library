---
id: computing-software.networking-hardware-and-wireless.unbound.unbound-control-cache-inspection-and-flushing
name: unbound-control-cache-inspection-and-flushing
category: computing-software
field: networking-hardware-and-wireless
product: unbound
tags: [networking-hardware-and-wireless, unbound, unbound-control, flush, flush-zone, dump-cache, cache-lookup]
level: practitioner
status: docs-checked
description: "Inspect and flush Unbound's cache with unbound-control: cache_lookup, dump_cache, load_cache, flush, flush_type, flush_zone, flush_bogus and flush_negative."
sources:
  - https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound-control.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# unbound-control cache inspection and flushing
Inspect:
- `cache_lookup [+t] names` prints RRsets and messages at or under each name (plus subnet-cache entries); `+t` allows TLD and root names, which is slow.
- `dump_cache` prints the cache as text; `load_cache` reads that format from stdin, meant for debugging, since wrong data can be served. Neither works on a remote multi-process Unbound.
- `lookup name` shows the nameservers that would be used.

Flush (each accepts `+c` to also remove cachedb entries):
- `flush [+c] name` removes A, AAAA, NS, SOA, CNAME, DNAME, MX, PTR, SRV, NAPTR, SVCB and HTTPS for the name.
- `flush_type [+c] name type` removes one type.
- `flush_zone [+c] name` removes everything at or below the name; slow because the whole cache is scanned. Entries are marked expired, so serve-expired can still answer while prefetching.
- `flush_bogus [+c]` removes bogus data.
- `flush_negative [+c]` removes NXDOMAIN, NODATA and SERVFAIL answers, bad key entries and iterator last-resort failures.

Related: `flush_requestlist` drops in-flight queries without touching the cache; `flush_infra` clears host data.

## Checked

2026-11-08. Read the unbound-control manual page source in full; all claims match it.

Method: documentation only; no commands were run.
