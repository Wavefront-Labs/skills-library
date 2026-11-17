---
id: computing-software.systems-network-administration.dns-dhcp.bind-statistics-channel-monitoring
name: bind-statistics-channel-monitoring
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dns, bind, dns-security, statistics-channels, rndc-stats, bind-exporter, prometheus, servfail-rate, query-rate, recursive-clients, dns-monitoring, named-stats]
level: practitioner
status: docs-checked
description: "Monitor BIND with the statistics channel and rndc stats: enabling JSON/XML stats, key counters (QPS, SERVFAIL, recursive clients, cache), Prometheus bind_exporter and alert ideas."
sources:
  - https://bind9.readthedocs.io/en/latest/reference.html
  - https://github.com/prometheus-community/bind_exporter
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# BIND statistics channel and monitoring

## Enable
```
statistics-channels {
    inet 127.0.0.1 port 8053 allow { 127.0.0.1; };      // keep it local or behind ACL
};
options { zone-statistics full; };                      // default is terse (name, serial, transfers only)
```
Endpoints: `http://127.0.0.1:8053/json` (full set) with subsets `/json/v1/status`, `/json/v1/server`,
`/json/v1/zones`, `/json/v1/xfrins`, `/json/v1/net`, `/json/v1/mem`, `/json/v1/traffic`; XML is at
`/xml` and `/xml/v3/...`. Needs BIND built with json-c and/or libxml2; with no `allow` clause any address can connect. Querying too often can slow query processing. Alternative: `rndc stats` dumps to the `statistics-file`.

## Counters that matter
| Counter | Why |
|---|---|
| `QryUDP`, `QryTCP` (also `QryDoT`, `QryDoH`) | query rate (diff over time = QPS) |
| `QrySERVFAIL` | resolution failures: upstream problems, DNSSEC bogus, lame servers |
| `QryNXDOMAIN` | typo traffic, random-subdomain attacks |
| `QryRecursion`, `QryDropped` | resolver load and drops |
| `QueryTimeout`, `Retry` | upstream reachability |
| `ValFail` | DNSSEC validation failures |
| `RateDropped`, `RateSlipped` | RRL activity |
| zone serial and `XfrSuccess`/`XfrFail` | secondary freshness (needs `zone-statistics full` for the counters) |

## Prometheus
The prometheus-community `bind_exporter` reads the channel (`--bind.stats-url`, default `http://localhost:8053/`; `--bind.stats-version` json by default, or xml, xml.v3, auto) and listens on `:9119` with metrics at `/metrics`. Example alert ideas:
- SERVFAIL ratio > 2% of responses for 10 min.
- Recursive load approaching the `recursive-clients` limit (see `rndc recursing`).
- QPS 3x above the weekly baseline (attack or misbehaving client).
- Secondary serial lagging primary for > 2 refresh intervals.
Dashboards: per-rcode rates, QPS by transport (UDP/TCP/DoT/DoH), cache hit ratio.

## Find the top clients/names during an incident
`rndc recursing` dumps the queries being recursed and the servers being queried; enable `rndc querylog on` briefly (heavy) and turn it off again.

## Verify
- [ ] JSON endpoint reachable locally only; exporter metrics in Prometheus.
- [ ] Alert for SERVFAIL ratio fires in a test (e.g. query a deliberately broken DNSSEC domain in a loop).

## Checked

Date: 2026-10-26. BIND 9 ARM sources in isc-projects/bind9 (main, 9.21 development line, latest tag v9.21.27, plus bind-9.20 branch notes and grammar), read on 2026-10-26. Confirmed: statistics-channels grammar and caveats, JSON and XML endpoint paths, zone-statistics default terse and full, counter names QryUDP/QryTCP/QryDoT/QryDoH/QrySERVFAIL/QryNXDOMAIN/QryRecursion/QryDropped/QueryTimeout/Retry/ValFail/RateDropped/RateSlipped/XfrSuccess/XfrFail, rndc recursing. prometheus-community/bind_exporter source (pushed 2026-10-14): flags --bind.stats-url, --bind.stats-version, default :9119 and /metrics. Removed unconfirmed JSON paths, cache-hit path and the packet-capture pipeline.

Method: documentation only; no commands were run.
