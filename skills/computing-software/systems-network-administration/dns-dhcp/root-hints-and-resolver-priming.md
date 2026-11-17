---
id: computing-software.systems-network-administration.dns-dhcp.root-hints-and-resolver-priming
name: root-hints-and-resolver-priming
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dns, root-hints, priming, resolver, named-root, bind]
level: practitioner
status: verified
description: "Maintain root hints and understand resolver priming: the hints file, priming queries, keeping hints current, and failures when hints or root access break."
sources:
  - https://www.rfc-editor.org/rfc/rfc9609
  - https://www.internic.net/domain/named.root
  - https://bind9.readthedocs.io/en/latest/reference.html#namedconf-statement-hint
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Root hints and priming

A recursive resolver needs a starting point: the root server names and addresses (root hints).
At startup it sends a **priming query** (`. NS` to one hint address) and caches the current root NS
set and glue; the hints only bootstrap that.

## Where hints live
| Software | Hints |
|----------|-------|
| BIND | built-in; override with `zone "." { type hint; file "named.root"; };` |
| Unbound | built-in; `root-hints: "/etc/unbound/root.hints"` to override |
| Windows DNS | Root Hints tab; `Get-DnsServerRootHint` (DnsServer module) lists them |
| PowerDNS Recursor | built-in; `hint-file` (empty = built-in hints; `no` / `no-refresh` disable processing) |

Current file: `https://www.internic.net/domain/named.root` (header "last update: October 21, 2026" when fetched). Update
when the root server operators announce an address change: b.root has renumbered, and named.root now lists
`170.247.170.2` / `2801:1b8:10::b` while RFC 8806 still shows the old `199.9.14.201`. Stale hints still work as long as
one address answers, but remove dead ones. Unbound's docs warn that its built-in default may become outdated.

## Check priming
```
dig @<resolver> . NS                              # should list a-m.root-servers.net with glue
dig +norecurse @198.41.0.4 . NS                   # direct to a.root
unbound-control lookup .
rndc dumpdb -cache && grep -A15 '^\. ' /var/named/data/cache_dump.db
```
RFC 9609: the priming query is `. NS` over UDP or TCP (random source port when UDP); send it only when needed,
that is with an empty cache or when the root NS RRset has expired (pre-fetching is allowed); if there is no response,
retry with a different configured address. The root NS RRset is signed, but at publication the root-servers.net
A and AAAA records were not, so they cannot be validated.

## Failure modes
- Resolver behind a firewall that blocks outbound 53 to arbitrary IPs: priming fails, every query
  SERVFAILs. Use forwarders instead, or open egress.
- Windows DNS with forwarders and "Use root hints if no forwarders are available" off: forwarder
  outage = total failure.
- Local root zone (RFC 8806) bypasses priming entirely.

## Verify
- [ ] `dig @resolver . NS +dnssec` returns the 13 root names (a-m) with an RRSIG (validating resolver).
