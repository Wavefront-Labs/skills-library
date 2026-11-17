---
id: computing-software.cloud-infrastructure-engineering.grafana-mimir.grafana-mimir-dns-service-discovery
name: grafana-mimir-dns-service-discovery
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-mimir
tags: [dns, service-discovery, memcached, dnssrv, memberlist-join]
level: practitioner
status: docs-checked
description: "Explains Mimir DNS service discovery prefixes (dns+, dnssrv+, dnssrvnoa+), where they are supported and the fully qualified name requirement."
sources: ["https://grafana.com/docs/mimir/latest/configure/about-dns-service-discovery/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# DNS service discovery in Mimir

Some Mimir clients locate backends through DNS. Search domains are not supported, so every name must be fully qualified.

## Where it works

- Memcached addresses: the blocks-storage chunks, index and metadata caches (`-blocks-storage.bucket-store.*-cache.memcached.addresses`) and `-query-frontend.results-cache.memcached.addresses`.
- Memberlist: `-memberlist.join`.
- The Alertmanager URL in the ruler: `-ruler.alertmanager-url`.

## Prefixes

- `dns+`: A/AAAA lookup, for example `dns+memcached.local:11211`.
- `dnssrv+`: SRV query, then each record is resolved as A/AAAA, for example `dnssrv+_memcached._tcp.memcached.namespace.svc.cluster.local`.
- `dnssrvnoa+`: SRV query only, with no A/AAAA lookup.

The Alertmanager URL must include the scheme, as in `dns+http://alertmanager.local:8080`.

Without a prefix the IP or hostname is used as given, without pre-resolving.

Memcached discovery with any of the three prefixes needs DNS over TCP: make sure Mimir can reach the DNS servers listed in `/etc/resolv.conf` over TCP on port `53`, through any firewall, network policy or service mesh. A successful UDP lookup does not prove TCP works.

## Checked

Confirmed the supported flags, the three prefixes with their lookup behaviour and examples, the scheme requirement for the Alertmanager URL, the unprefixed behaviour and the fully qualified name rule. Removed the Kubernetes headless Service remark and the cross-skill reference because the page does not state them. Added the DNS over TCP requirement from the page.

Method: docs-checked 2026-11-09 against the raw grafana/mimir docs page about-dns-service-discovery.md, read in full.
