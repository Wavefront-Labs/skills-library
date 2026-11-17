---
id: computing-software.systems-network-administration.dns-dhcp.round-robin-a-aaaa-records
name: round-robin-a-aaaa-records
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dns, round-robin-dns, a-record, aaaa-record, load-distribution]
level: practitioner
status: verified
description: "Use multiple A/AAAA records for simple load distribution: rrset ordering, client behaviour, TTL choices, failure handling and when to use a real load balancer."
sources:
  - https://www.rfc-editor.org/rfc/rfc1794
  - https://www.rfc-editor.org/rfc/rfc6724
  - https://bind9.readthedocs.io/en/latest/reference.html#namedconf-statement-rrset-order
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# A/AAAA and round-robin

Several A (or AAAA) records for one name spread clients across servers:
```
www   300  IN A  192.0.2.10
www   300  IN A  192.0.2.11
www   300  IN A  192.0.2.12
```

## Ordering
- Authoritative servers and resolvers rotate or randomise the RRset order. BIND's current ARM: with no
  `rrset-order` statement the implicit default is `cyclic` (offset based on the query ID); `random` is deprecated and
  behaves exactly like `cyclic`; `none` returns database order; if any `rrset-order` statement exists but no rule
  matches an RRset, that RRset gets `none`. There is no `fixed` keyword in the current ARM. CoreDNS's `loadbalance`
  plugin (policy `round_robin`) reordered three A records differently across queries in a local test.
- Clients do not always take the first record: RFC 6724 rule 9 prefers the destination with the longest matching
  prefix with the source address (when both are IPv6 or both IPv4), so clients in 192.0.2.0/24 may all pick the
  same server. glibc `/etc/gai.conf` and Windows have different rules.
- Caching resolvers serve one cached order to many clients for the TTL.

## What it is not
- Not health-checked: a dead server keeps getting its share until the record is removed and TTLs
  expire. Whether a client retries the next address depends on the application.
- Not weighted: to weight, repeat addresses (crude) or use provider weighted records / SRV weights.
- Not session-sticky.

## Practical guidance
- Short TTL (60-300 s) if you plan to pull records during failures; automate removal with health
  checks (a DNS provider's health-checked records, or a script with nsupdate).
- Mix of A and AAAA: dual-stack clients can use Happy Eyeballs (RFC 8305), which limits the delay from a broken IPv6 address.
- For real balancing, put a load balancer or anycast VIP behind one name.

## Check
```
for i in 1 2 3; do dig +short www.example.com A @ns1.example.com; echo; done
```

## Verify
- [ ] Access logs on each server show roughly even shares over a day, and removal of one record drains it within TTL.
