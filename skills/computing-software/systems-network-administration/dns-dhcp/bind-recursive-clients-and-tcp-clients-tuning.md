---
id: computing-software.systems-network-administration.dns-dhcp.bind-recursive-clients-and-tcp-clients-tuning
name: bind-recursive-clients-and-tcp-clients-tuning
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dns, bind, tcp-clients, recursive-clients, performance-tuning]
level: practitioner
status: docs-checked
description: "Tune BIND client limits: recursive-clients, tcp-clients, clients-per-query, fetches-per-zone/server, and read the logs that show limits being hit."
sources:
  - https://bind9.readthedocs.io/en/latest/reference.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# recursive-clients and tcp-clients tuning

Default limits are conservative; busy resolvers hit them and start dropping queries.

## The knobs
```
options {
    recursive-clients 10000;     // default 1000: simultaneous recursive lookups (hard quota)
    tcp-clients 1000;            // default 150: simultaneous client TCP connections
    clients-per-query 10;        // default 10: initial per-query client limit, adapts up to max-clients-per-query
    max-clients-per-query 100;   // ceiling for the adaptive estimate
    fetches-per-zone 200;        // limit iterative fetches to one zone; keep below recursive-clients
    fetches-per-server 400;      // per upstream server; default 0 = unlimited
    tcp-listen-queue 100;        // default and minimum 10
    tcp-idle-timeout 300;        // units of 100 ms: default 300 (30 s), maximum 1200
};
```

## Signs you hit limits
Look for quota-reached messages in the server log (the `client` and `resolver` categories) and
fetch-limit messages for `fetches-per-zone` / `fetches-per-server`. The statistics channel exposes
resolver counters such as `ZoneQuota`, `QueryTimeout` and `Retry`; `rndc recursing` dumps the queries
currently being recursed.

## Sizing
- recursive-clients: estimate as peak cache-miss QPS x average recursion time (5,000 cache-miss QPS at
  200 ms upstream is about 1,000 concurrent), plus headroom. Each recursing client uses on the order of
  20 KB, so lower it on small hosts.
- tcp-clients: raise if many clients use TCP (truncated answers, large DNSSEC responses).

## Gotchas
- Raising limits hides upstream problems (unreachable authoritative servers stall slots); check
  fetch timeouts first.
- `fetches-per-zone` and `fetches-per-server` should be smaller than `recursive-clients`; they protect against floods aimed at one zone or server but can block legitimate busy zones; watch the `ZoneQuota` counter.

## Verify
- [ ] Under peak load, quota messages are gone and the resolver counters stay quiet.

## Checked

Date: 2026-10-26. BIND 9 ARM sources in isc-projects/bind9 (main, 9.21 development line, latest tag v9.21.27, plus bind-9.20 branch notes and grammar), read on 2026-10-26. Confirmed in reference.rst: defaults recursive-clients 1000 (about 20 KB each), tcp-clients 150, clients-per-query 10 with max-clients-per-query adaptation, fetches-per-server default 0, fetches-per-zone/server should be below recursive-clients, tcp-listen-queue default and minimum 10, tcp-idle-timeout in 100 ms units (default 300, max 1200), resolver counters ZoneQuota/QueryTimeout/Retry, rndc recursing. Removed unconfirmed log message strings and counters (RecursClients, TCPConnHighWater) that the ARM does not list.

Method: documentation only; no commands were run.
