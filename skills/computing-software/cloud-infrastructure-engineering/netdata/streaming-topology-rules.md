---
id: computing-software.cloud-infrastructure-engineering.netdata.streaming-topology-rules
name: streaming-topology-rules
category: computing-software
field: cloud-infrastructure-engineering
product: netdata
tags: [netdata, thin-mode, parent-hierarchy, grand-parent]
level: practitioner
status: docs-checked
description: "Netdata streaming topology rules: one Parent per Child at a time, Full versus Thin Child modes, standalone, cluster and proxy Parents, and Parent behaviour."
sources:
  - https://raw.githubusercontent.com/netdata/netdata/master/docs/observability-centralization-points/metrics-centralization-points/README.md
  - https://raw.githubusercontent.com/netdata/netdata/master/docs/observability-centralization-points/metrics-centralization-points/faq.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Rules:
- A Child streams to only one Parent at a time; listing several gives failover, and only the first working one is used.
- A Parent can receive from many Children and re-stream to a Grand Parent.
- Streaming copies recent past samples (replication) and real-time samples.

Child modes:
- Full (default): machine learning, alerts, notifications, dashboard all on.
- Thin: collects and forwards only, with some local retention for network issues.

Child settings you can disable: ML, alerts, API and dashboard, exporting; retention can be minimal in `ram` or `alloc` mode.

Parent types: Standalone (single or top-most), Cluster (circular, top level only), Proxy (stores and forwards upward).

Parent behaviour: stores metrics with its own retention, runs anomaly detection and alerting for all connected systems, exports all metrics, forwards Functions requests to Children (which must be online), and registers Children with Cloud when claimed.

Not possible or not recommended:
- HTTP proxy between Parent and Child (streaming is not HTTP).
- TCP load balancer across Parents is not recommended; list the Parents in the Child `stream.conf` instead.

Child retention need: about 5 to 10 minutes in `alloc` mode with a Parent cluster; use `dbengine` for a single Parent.

## Checked

2026-11-04: one Parent per Child, failover, re-streaming, replication, Full and Thin modes, Parent types, Parent capabilities, the feature comparison, the HTTP proxy and load balancer FAQ answers and the Child retention guidance confirmed against the Netdata metrics centralization README and FAQ. Changed the load balancer line from not supported to not recommended, as the FAQ words it.

Method: documentation only; no commands were run.
