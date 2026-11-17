---
id: computing-software.cloud-infrastructure-engineering.fluentd.high-availability-forwarder-aggregator
name: high-availability-forwarder-aggregator
category: computing-software
field: cloud-infrastructure-engineering
product: fluentd
tags: [cloud-infrastructure-engineering, fluentd, high-availability, forwarder, aggregator, standby, at-least-once, no-nodes-available]
level: advanced
status: docs-checked
description: "Design Fluentd HA with log forwarders and aggregators: out_forward primary plus standby server, buffering, failure windows, and the no nodes are available error."
sources:
  - https://docs.fluentd.org/deployment/high-availability
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fluentd high availability
Delivery: Fluentd offers at-most-once and at-least-once (exactly-once would require synchronous logging that stops ingestion); logging is asynchronous to avoid hurting applications.

Topology: **forwarders** on every node receive local events and forward them; **aggregators** receive, buffer and upload to the cloud. Fluent Bit is suggested as a light forwarder.

Forwarder config (active 192.168.0.1, backup 192.168.0.2):
```
<match mytag.**>
  @type forward
  <server>
    host 192.168.0.1
    port 24224
  </server>
  <server>
    host 192.168.0.2
    port 24224
    standby
  </server>
  <buffer>
    flush_interval 60s
  </buffer>
</match>
```
Longer `flush_interval` lowers CPU but raises latency. If both aggregators die, forwarders buffer on disk. Aggregators use `<source> @type forward` and a buffered output; failed uploads stay on local disk until retransmitted.

Data loss windows (forwarder and aggregator alike): process dies after receiving events but before writing them to the buffer; disk failure destroys the file buffer.

**"no nodes are available"**: check port 24224 over TCP and UDP (heartbeat), e.g. `telnet host 24224` and `nmap -p 24224 -sU host`. The page notes a known VMware issue that sometimes drops small UDP heartbeat packets.

## Checked

2026-11-04. Confirmed against the Fluentd High Availability Config page (docs.fluentd.org/deployment/high-availability): delivery semantics, topology, forwarder config, aggregator behaviour, loss windows, the no nodes are available checks. Nothing removed.

Method: documentation only; no commands were run.
