---
id: computing-software.cloud-infrastructure-engineering.cortex.distributor-validation-and-load-balancing
name: distributor-validation-and-load-balancing
category: computing-software
field: cloud-infrastructure-engineering
product: cortex
tags: [distributor, write-path, validation, quorum, load-balancing]
level: practitioner
status: docs-checked
description: "Explain what the Cortex distributor validates, how writes reach a quorum of ingesters, and how to load balance it."
sources:
  - https://github.com/cortexproject/cortex/blob/master/docs/architecture.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The distributor is the first stop in the write path. For each incoming sample it checks correctness against the tenant's limits (falling back to defaults when no override exists). Validation covers: label names are formally valid, the maximum number of labels per metric is respected, maximum label name and value lengths are respected, and the timestamp is within the configured min/max range.

Distributors are stateless and scale freely.

Series are placed on ingesters using consistent hashing with a configurable replication factor. Because all distributors share the same hash ring, write requests can go to any distributor and you can use a stateless load balancer; random load balancing across distributors is recommended (for example a Kubernetes Service).

Writes use Dynamo-style quorum consistency: the distributor waits for a positive response from at least half plus one of the ingesters a sample was sent to before answering the Prometheus write request successfully.

## Checked

Method: docs-checked 2026-11-09 against the Cortex architecture page (raw markdown, read in full). The worked example of a 2-of-3 quorum was dropped as not stated on the page.
