---
id: computing-software.cloud-infrastructure-engineering.victoriametrics.victoriametrics-vmagent-sharding-and-ha
name: victoriametrics-vmagent-sharding-and-ha
category: computing-software
field: cloud-infrastructure-engineering
product: victoriametrics
tags: [vmagent, sharding, high-availability, promscrape-cluster, shard-by-url, dedup]
level: advanced
status: docs-checked
description: "Shard scrape targets across vmagent replicas and write shards or replicas to several backends with the cluster flags."
sources: ["https://docs.victoriametrics.com/victoriametrics/vmagent/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Victoriametrics vmagent sharding and ha

Spread scraping over several vmagent instances with `-promscrape.cluster.*`:
- `-promscrape.cluster.membersCount`: total number of instances.
- `-promscrape.cluster.memberNum`: this instance index, `0` to `N-1` (in Kubernetes it can be a StatefulSet pod name ending in a number).
- `-promscrape.cluster.replicationFactor`: how many instances scrape each target (HA).
- `-promscrape.cluster.shardByLabels`: shard by specific labels; `-promscrape.cluster.memberLabel` names the label carrying the member number.
- `-promscrape.cluster.memberURLTemplate`: builds links on `/service-discovery`, with `%d` replaced by the member number.
- `-promscrape.cluster.name`: set per instance in HA setups.
- `-dedup.minScrapeInterval` must match `scrape_interval` when several instances scrape the same target.

Spread series over several remote write targets:
- `-remoteWrite.shardByURL` distributes series across `-remoteWrite.url` destinations.
- `-remoteWrite.shardByURLReplicas=N` writes each sample to N destinations.
- `-remoteWrite.shardByURL.labels` and `-remoteWrite.shardByURL.ignoreLabels` are mutually exclusive label-based options.

Plain replication needs no sharding flags: pass several `-remoteWrite.url` values. Troubleshooting aids: `-promscrape.maxDroppedTargets` controls how many dropped targets `/service-discovery` shows, and `-promscrape.noStaleMarkers` disables staleness markers.

## Checked

2026-11-03. Flags, endpoints, HTTP paths, defaults, limits and version gates were checked against the official VictoriaMetrics documentation pages cited in `sources` (docs.victoriametrics.com, fetched this batch) with a phrase-by-phrase comparison. No wrong claims were found; no claims were removed.

Method: documentation only; no commands were run.
