---
id: computing-software.systems-network-administration.dns-dhcp.search-domains-and-ndots
name: search-domains-and-ndots
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dns, search-domain, ndots, resolv-conf, stub-resolver, kubernetes-dns, dns-suffix]
level: practitioner
status: docs-checked
description: "Understand stub resolver search lists and ndots: how short names expand, the Kubernetes ndots:5 query storm and its fixes, and diagnosing slow or wrong lookups."
sources:
  - https://man7.org/linux/man-pages/man5/resolv.conf.5.html
  - https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/
  - https://www.rfc-editor.org/rfc/rfc1034
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Search domains and ndots

## Linux stub resolver
`/etc/resolv.conf`:
```
nameserver 10.0.0.53
search corp.example.net example.net
options ndots:1 timeout:2 attempts:2
```
- A name with fewer dots than `ndots` is tried with each search suffix first, then as is.
- A name with at least `ndots` dots is tried as is first, then with suffixes.
- A trailing dot (`host.example.net.`) means absolute: no search list.

## Kubernetes ndots:5
Pods get `search <namespace>.svc.cluster.local svc.cluster.local cluster.local` and
`options ndots:5`. A lookup of `api.example.com` (2 dots, fewer than 5) is first tried with each
search suffix appended (`api.example.com.<namespace>.svc.cluster.local`, ...), so several NXDOMAIN
answers come back before the real one. Effects: extra DNS load and latency.
Fixes:
- Use FQDNs with a trailing dot in app config (`api.example.com.`).
- Per pod: `dnsConfig: options: [{name: ndots, value: "2"}]`.

## Typical faults
- Wrong host answers for a short name: a suffix earlier in the list has a matching record (or a
  wildcard). Use FQDNs.
- Slow lookups: each suffix times out against an unreachable server, or long NXDOMAIN chains.

## Verify
- [ ] A packet capture shows the expected number of queries and the first query succeeds for FQDNs.

## Checked
2026-10-28. Confirmed against the resolv.conf(5) man page: search list used for names with fewer than `ndots` dots, `ndots` default 1, `timeout`/`attempts` options. Confirmed against the Kubernetes DNS for Services and Pods page: pod search list and `options ndots:5`, `dnsConfig` ndots override. Removed as unconfirmed: the Windows suffix search section, `dig +search`, macOS `scutil` note, NodeLocal DNSCache, conntrack claim and the query-count figure.
Method: documentation only; no commands were run.
