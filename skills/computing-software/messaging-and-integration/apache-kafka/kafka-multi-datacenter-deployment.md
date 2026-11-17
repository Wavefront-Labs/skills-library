---
id: computing-software.messaging-and-integration.apache-kafka.kafka-multi-datacenter-deployment
name: kafka-multi-datacenter-deployment
category: computing-software
field: messaging-and-integration
product: apache-kafka
tags: [apache-kafka, multi-datacenter, socket-send-buffer-bytes, socket-receive-buffer-bytes]
level: practitioner
status: docs-checked
description: "Deploy one Kafka cluster per datacenter with mirroring, plus aggregate clusters, and tune TCP socket buffers over the WAN."
sources:
  - https://kafka.apache.org/42/operations/datacenters/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: choose a multi-datacenter topology.

Recommended pattern: run a local Kafka cluster in each datacenter. Applications talk only to their local cluster, and data is mirrored between clusters (see Geo-Replication). Each facility can stand alone and keep running if inter-datacenter links fail; mirroring simply falls behind and catches up when the link returns. Inter-datacenter replication is managed and tuned centrally.

For a global view, mirror each local cluster into an aggregate cluster used for reads by applications that need the full data set.

Alternative: read from or write to a remote cluster across the WAN, accepting the added latency. Kafka batches in both producer and consumer, so it can still reach high throughput over high-latency links; you may need to raise the TCP socket buffers with `socket.send.buffer.bytes` and `socket.receive.buffer.bytes` on the producer, consumer and broker.

Avoid: a single Kafka cluster stretched across datacenters over a high-latency link. It causes very high replication latency for writes, and Kafka will not remain available in all locations if the network between them fails.

## Checked

Method: 2026-11-08 docs-only read of the cited Kafka 4.2 datacenters page. All claims matched; no content changes. No hands-on run.
