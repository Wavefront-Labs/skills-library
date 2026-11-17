---
id: computing-software.data-engineering.apache-nifi.process-group-flowfile-concurrency
name: process-group-flowfile-concurrency
category: computing-software
field: data-engineering
product: apache-nifi
tags: [data-engineering, apache-nifi, process-groups, flowfile-concurrency, outbound-policy, batch-output]
level: advanced
status: docs-checked
description: "Process Group General tab: FlowFile Concurrency (unbounded, single FlowFile or single batch per node), Outbound Policy, batch.output attributes and default connection settings."
sources:
  - https://nifi.apache.org/docs/nifi-docs/html/user-guide.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Process group concurrency

The Process Group configuration dialog includes Name, Parameter Context, FlowFile Concurrency, Outbound Policy, and default connection settings (FlowFile expiration and back pressure thresholds).

- FlowFile Concurrency controls how data enters the group through Input Ports: Unbounded (default), Single FlowFile Per Node, or Single Batch Per Node.
  - Single FlowFile Per Node: one FlowFile is admitted; no more enter until all FlowFiles have left the group (removed, auto-terminated or sent out an Output Port).
  - Single Batch Per Node: like the above, but once a FlowFile is ingested the ports keep ingesting until the queues feeding them are empty, then admit nothing more until all data has finished and left the group.
  - It controls only Input Port intake; it does not stop a processor inside the group ingesting data from outside NiFi.
- Outbound Policy: Stream When Available (default) transfers data out immediately; Batch Output holds all data until everything in the group is queued at Output Ports. It is ignored when concurrency is Unbounded.
- With Batch Output, each FlowFile leaving gets attributes `batch.output.<Port Name>` holding the number of FlowFiles routed to that port (example: batch.output.A = 2, B = 1, C = 2, D = 0).
- Default connection settings affect only new connections in the group, not existing ones.
- Caveats from the guide: with Single FlowFile Per Node each node can admit its own FlowFile (a 5-node cluster may process up to 5 at once), and load-balanced connections inside a non-Unbounded group are not recommended.
- Batch Output with a back pressure threshold on the connection into an Output Port can deadlock; raise or disable (0) that threshold.

Verify: with Single FlowFile Per Node, the group admits one FlowFile at a time until it exits.

## Checked

Confirmed against the NiFi user guide sections on Process Group configuration (FlowFile Concurrency, Outbound Policy, Connecting Batch-Oriented Process Groups, Caveats, Default Settings for Connections).

Method: docs-only read of cited pages, 2026-11-08
