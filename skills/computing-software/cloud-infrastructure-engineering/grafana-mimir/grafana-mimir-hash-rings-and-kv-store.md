---
id: computing-software.cloud-infrastructure-engineering.grafana-mimir.grafana-mimir-hash-rings-and-kv-store
name: grafana-mimir-hash-rings-and-kv-store
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-mimir
tags: [hash-ring, memberlist, consul, etcd, kv-store, sharding]
level: advanced
status: docs-checked
description: "Covers Mimir hash rings per component, the key-value store backends, memberlist join and bind settings, and cluster label verification."
sources: ["https://grafana.com/docs/mimir/latest/configure/configure-hash-rings/", "https://grafana.com/docs/mimir/latest/configure/about-dns-service-discovery/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Hash rings and the KV store

Mimir uses consistent-hashing rings for sharding, replication and service discovery. Each component builds its own ring, configured by flag prefix:

- Ingesters `-ingester.ring.*`; ingest-storage partitions `-ingester.partition-ring.*`
- Distributors `-distributor.ring.*`; compactors `-compactor.ring.*`
- Store-gateways `-store-gateway.sharding-ring.*`
- Optional: query-schedulers `-query-scheduler.ring.*`, rulers `-ruler.ring.*`, Alertmanagers `-alertmanager.sharding-ring.*`, overrides-exporters `-overrides-exporter.ring.*`

## KV store

Set `<prefix>.store` to `memberlist` (default), `consul`, `etcd` or `multi`.

## Memberlist

An instance joins by resolving `-memberlist.join` (repeatable): `ip:port`, `hostname:port` or a DNS service discovery address. Default port is 7946. Memberlist is configured globally, not per component. On Kubernetes use a headless Service and `dnssrv+<service>.<namespace>.svc.cluster.local:<port>`.

If port 7946 is taken or several processes share a node, change `-memberlist.bind-addr`, `-memberlist.bind-port`, `-memberlist.advertise-addr`, `-memberlist.advertise-port`.

## Cluster label verification

By default a joining instance accepts any discovered peer, which can merge unrelated Mimir clusters or other memberlist systems. With cluster label verification, all memberlist traffic carries the configured label and non-matching traffic is discarded.

## DNS prefixes

`dns+` (A/AAAA), `dnssrv+` (SRV then A/AAAA), `dnssrvnoa+` (SRV only). Search domains are unsupported; use fully qualified names. No prefix means no pre-resolution.

## Checked

Confirmed against both pages: ring flag prefixes, KV backends and `<prefix>.store`, memberlist join forms, default port 7946, global memberlist, Kubernetes headless Service form, bind and advertise flags, cluster label verification, DNS prefixes and the search-domain limitation. Nothing removed.

Method: docs-checked 2026-11-09 against the raw markdown of the Mimir configure-hash-rings and about-dns-service-discovery pages (grafana/mimir main), read in full.
