---
id: computing-software.systems-network-administration.dns-dhcp.dnsperf-load-testing
name: dnsperf-load-testing
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dns, dns-security, dnsperf, resperf, load-testing, capacity-planning, qps, latency-percentiles, query-file, flamethrower, dns-benchmark]
level: practitioner
status: docs-checked
description: "Load-test DNS with dnsperf and resperf: realistic query files from captures, authoritative vs resolver tests, reading QPS, loss and latency, safe practice."
sources:
  - https://github.com/DNS-OARC/dnsperf
  - https://www.dns-oarc.net/tools/dnsperf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DNS load testing with dnsperf

## Tools
- `dnsperf`: sends queries from a file at a set concurrency/rate; measures throughput and latency.
  Best for **authoritative** servers and fixed workloads.
- `resperf`: ramps the query rate up linearly to a target maximum while watching for loss; for **resolvers** (cache misses matter). Set `-m` higher than the server's expected maximum throughput.
Both are DNS-OARC tools.

## Query file
Format: one line per query, a domain name and a record type:
```
www.example.org A
example.org MX
api.example.org AAAA
```
The man page says the file should be a large, realistic set of queries (mostly queries for types you actually see); build it from your own traffic so the cache-hit ratio and name mix are realistic.

## Run
```
dnsperf -s 10.0.0.53 -d queries.txt -l 60 -c 20 -Q 20000      # 60 s limit, 20 clients, cap 20k QPS
dnsperf -s 10.0.0.53 -d queries.txt -l 60 -m tcp               # transport mode: udp, tcp, dot or doh
resperf -s 10.0.0.53 -d queries.txt -m 50000 -r 60             # ramp to a 50k QPS maximum over 60 s (default 60 s)
```
Read the end-of-run statistics (queries sent, completed and lost, throughput, latency, response codes). With resperf's `-P plot_data_file` look at latency and loss as the rate climbs: where latency rises and loss starts is the practical capacity; leave headroom below it. For DoH, set `-O doh-uri=...`.

## Practice
- Test from **multiple** generator hosts if one client saturates first (check its CPU); `-c` sets the number of client sockets and `-T` the threads.
- Never test production resolvers at peak, or third-party/internet authoritatives (that is an attack).
- For resolvers, results depend on upstream latency and cache warmth: test warm and cold.
- Record versions, config, hardware, query file stats with the results.

## Verify
- [ ] Capacity figure (QPS at acceptable latency and loss) documented per server type.
- [ ] Generator was not the bottleneck (check its CPU).

## Checked

Date: 2026-10-26. Documentation: DNS-OARC/dnsperf repository man page sources src/dnsperf.1.in and src/resperf.1.in and README, read 2026-10-26. Confirmed: dnsperf options -s -d -l -c -Q -m (udp, tcp, dot, doh) -T, -O doh-uri, input-file format and guidance, resperf options -m -r (default 60 s) -P. Removed the unconfirmed flamethrower, packaging, tshark pipeline, output label and percentage-headroom claims.

Method: documentation only; no commands were run.
