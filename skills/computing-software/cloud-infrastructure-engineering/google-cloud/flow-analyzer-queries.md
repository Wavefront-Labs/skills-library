---
id: computing-software.cloud-infrastructure-engineering.google-cloud.flow-analyzer-queries
name: flow-analyzer-queries
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, network-intelligence-center, flow-analyzer, vpc-flow-logs, log-analytics, top-talkers]
level: practitioner
status: docs-checked
description: "Use Network Intelligence Center Flow Analyzer to query VPC Flow Logs without writing SQL: prerequisites, aggregation modes, filters, display modes, sampling points and drill-down."
sources: ["https://cloud.google.com/network-intelligence-center/docs/flow-analyzer/overview", "https://cloud.google.com/vpc/docs/flow-logs"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Flow Analyzer queries

Flow Analyzer analyses VPC Flow Logs stored in a log bucket, with 5-tuple granularity (source IP, destination IP, source port, destination port, protocol). It is built on Observability Analytics and BigQuery, so you build queries from filters instead of writing SQL.

## Prerequisites
- VPC Flow Logs enabled, with the logs stored in a Cloud Logging bucket that has Observability (Log) Analytics enabled; you select the project holding that bucket.
- Flow logs can alternatively be routed to BigQuery or Pub/Sub, but Flow Analyzer queries the Analytics-enabled log bucket.
- Flow log settings that matter: the aggregation interval is configurable (5 seconds is the default; 30 seconds, 1, 5, 10 and 15 minutes are also offered), a secondary sampling rate is configurable, and metadata annotations can be turned off or trimmed to save storage.

## Building a query
1. Pick the time range (default one hour; presets, custom range, or centred on a timestamp).
2. Pick the traffic aggregation:
   - Source and destination: aggregates from source to destination using the SRC and DEST fields.
   - Client and server: tries to find the connection initiator (the smaller port number is the server; a resource with a `gke_service` definition counts as a server) and aggregates both directions.
3. Add basic filters (several values of one filter are ORed; separate filters are ANDed) or SQL filters (BigQuery SQL syntax) for field-to-field comparisons, nested boolean logic and IP functions.
4. Choose a display mode: Data volume (default; bytes sent or packets sent), Packet drops (drop rate or count) or Latency (round-trip time for TCP traffic from the flow logs).

Results show the Highest data flows chart (top five flows over time) and the All data flows table (top flows, up to 5,000 rows). The table can be sorted by total traffic, aggregate packets, packet drops or latency.

## Typical analyses
| Question | Configure |
|---|---|
| Top talkers | Source and destination aggregation, Data volume, Bytes sent, Total traffic |
| Spikes | Data volume with P95 or Maximum traffic rate |
| Dropped traffic | Packet drops mode; the All packet drop flows table has a Drop reason column |
| Slow flows | Latency mode, rank by P95, P99 or Max |
| Who is behind a flow | Details, then drill down by another field (for example source IP); Compare to past overlays earlier traffic |
| Paths to the internet | Flow details, Egress AS paths tab, filtered with the Egress AS path filter |

Explore in Log Analytics opens the underlying query in Observability Analytics for hand editing.

## Gotchas
- Bytes sent counts payload only (not headers), can be zero for header-only packets, and the data is sampled, so Google states you cannot use it to estimate costs. It is for ranking and trends.
- A VM-to-VM flow is reported at both endpoints when both subnets have flow logs; choose the Average of source and destination endpoint sampling point to avoid double counting (traffic in an alignment period reported at both ends is divided by two).
- Small alignment periods cost performance and make long ranges unreadable (a 1-minute alignment over 30 days gives more than 43,000 points); the range is 5 seconds to 1 day, with an Automatic mode.
- Primary packet sampling cannot be controlled and can miss short-lived or low-volume TCP connections; TCP connection logging is the optional fix.

## Checked
Confirmed 2026-11-08 against the Flow Analyzer overview and the VPC Flow Logs overview. Removed claims the pages do not state: the `gcloud logging buckets update` command, the required IAM roles, the sample SQL and its JSON field paths, the example sampling values, Private Google Access labelling, and the log-volume advice. The analyze-flow-logs source returned 404 and was dropped.
Method: docs-only read of cited pages, 2026-11-08
