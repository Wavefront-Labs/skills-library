---
id: computing-software.cybersecurity-defensive.splunk.indexer-clustering
name: indexer-clustering
category: computing-software
field: cybersecurity-defensive
product: splunk
tags: [splunk, splunk-architecture, indexer-clustering, cluster-manager, replication-factor, search-factor, server-conf, rolling-restart, bucket-fixup, maintenance-mode, multisite-clustering]
level: advanced
status: draft
description: "Build and operate a Splunk indexer cluster: replication and search factors, peer onboarding, maintenance mode, rolling restarts and bucket fix-up."
sources: ["Splunk Docs - Managing Indexers and Clusters of Indexers", "Splunk Docs - server.conf spec ([clustering] stanza)", "Splunk Validated Architectures"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Splunk indexer clustering

**Goal:** run indexers as a cluster that survives a peer loss without losing searchable
data, and change it (config pushes, upgrades, restarts) without a data outage.

## 1. Size the factors first
- **Replication factor (RF):** copies of each bucket's raw data. RF=3 tolerates 2 peer losses.
- **Search factor (SF):** copies that also hold searchable tsidx files. SF<=RF. SF=2 is the
  common choice: fast recovery without paying tsidx disk on every copy.
- Disk per peer is roughly `daily_ingest x retention_days x (RF x ~0.15 rawdata + SF x ~0.35 tsidx) / peers`
  (the Splunk rule of thumb of about 50% total compression). Measure with your own data after a week.
- Need at least RF peers (multisite: per-site `site_replication_factor = origin:2,total:3`).

## 2. Configure (server.conf)
Cluster manager:
```
[clustering]
mode = manager
replication_factor = 3
search_factor = 2
pass4SymmKey = <shared secret>
cluster_label = prod_idx
```
Each peer:
```
[replication_port://9887]

[clustering]
mode = peer
manager_uri = https://cm.example.internal:8089
pass4SymmKey = <shared secret>
```
Search heads: `mode = searchhead` with the same `manager_uri`. (Pre-9.0 versions use
`master`/`slave` and `master_uri`.) Forwarders should use indexer discovery
(`[indexer_discovery:...]` in outputs.conf) so new peers are picked up automatically.

## 3. Push configuration via the manager bundle
Put apps/indexes.conf in `$SPLUNK_HOME/etc/manager-apps/` on the manager, then:
```
splunk validate cluster-bundle --check-restart
splunk apply cluster-bundle --answer-yes
splunk show cluster-bundle-status
```
Never edit `etc/peer-apps` on a peer by hand; the next push overwrites it.

## 4. Planned work: maintenance mode and rolling restart
```
splunk enable maintenance-mode      # stops bucket fix-up while peers bounce
splunk rolling-restart cluster-peers -searchable true
splunk disable maintenance-mode
```
Searchable rolling restart keeps searches running but needs the cluster complete
(RF and SF met) before you start. Upgrade order: manager, then search heads, then peers.

## 5. Health
```
splunk show cluster-status --verbose
| rest /services/cluster/manager/fixup level=replication_factor
```
Watch "Replication factor met / Search factor met" and the fix-up queue. A persistently
growing pending fix-up list usually means disk full on a peer or a blocked replication port.

## Gotchas
- Mismatched `pass4SymmKey` gives a peer that never joins and only says so in splunkd.log.
- Use `splunk offline` (not `stop`) when retiring a peer, otherwise the cluster has to
  rebuild every bucket it held; `splunk offline --enforce-counts` waits until copies are safe.
- Leaving maintenance mode on after work silently disables fix-up: alert on it.
- indexes.conf must be identical on all peers; define custom indexes only in the bundle.

## Verify
- [ ] `show cluster-status` reports RF and SF met and all peers Up.
- [ ] Stopping one peer in a test window keeps all data searchable.
- [ ] Bundle validation runs clean before every push.
