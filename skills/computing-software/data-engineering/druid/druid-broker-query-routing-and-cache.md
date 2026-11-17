---
id: computing-software.data-engineering.druid.druid-broker-query-routing-and-cache
name: druid-broker-query-routing-and-cache
category: computing-software
field: data-engineering
product: druid
tags: [broker, query-routing, timeline, cache, memcached, realtime]
level: practitioner
status: docs-checked
description: "Describe how the Broker discovers segments, forwards queries and uses its per-segment cache."
sources:
  - https://github.com/apache/druid/blob/master/docs/design/broker.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The Broker routes queries in a distributed cluster and consolidates result sets from the individual data services. It discovers data-serving services through ZooKeeper, then polls each one over HTTP for the segments it is serving.

Forwarding queries: most queries carry an interval, and Druid partitions segments by time interval across the cluster. The Broker builds a timeline of segments for every datasource and the services that serve them. For each query it uses that view to pick which services to contact, so a query for more than one day may touch several Historicals and then be merged by the Broker.

Caching: Brokers can use a cache with LRU invalidation that stores per-segment results. The cache can be local to each Broker or shared through an external distributed cache such as memcached. When a query arrives, the Broker maps it to a set of segments. Results for some of those segments may already be cached; the Broker forwards the query only for the uncached ones to the Historicals, then stores the returned results in the cache. Real-time segments are never cached, so requests for real-time data always go to the real-time services.

Start with `org.apache.druid.cli.Main server broker`.

## Checked

2026-11-08. Read design/broker.md in full; claims match (ZooKeeper discovery of Historicals and Peons, timeline lookup, per-segment LRU cache, real-time never cached).

Method: documentation only; no commands were run.
