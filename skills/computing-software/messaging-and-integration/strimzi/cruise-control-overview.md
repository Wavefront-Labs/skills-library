---
id: computing-software.messaging-and-integration.strimzi.cruise-control-overview
name: cruise-control-overview
category: computing-software
field: messaging-and-integration
product: strimzi
tags: [cruise-control, optimization-goals, load-monitor]
level: advanced
status: docs-checked
description: "Know Cruise Control's components and what Strimzi uses it for."
sources: ["https://strimzi.io/docs/operators/latest/deploying.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Cruise Control overview

**Goal:** understand what Cruise Control does in a Strimzi cluster.

Four main components:

- **Load Monitor:** collects metrics and analyses cluster workload.
- **Analyzer:** generates optimization proposals from collected data and configured goals.
- **Anomaly Detector:** identifies irregularities.
- **Executor:** applies approved proposals.

Its REST API supports, through Strimzi: generating proposals from goals, rebalancing a cluster, changing topic replication factor, and reassigning partitions between JBOD disks.

Cruise Control self-healing is **not supported**. Notifiers or custom goals can be added by including JARs in a custom image based on the Strimzi Kafka image.

Deploy by adding `cruiseControl` to the `Kafka` resource; an empty object `{}` uses defaults.

```yaml
spec:
  cruiseControl:
    brokerCapacity:
      inboundNetwork: 10000KB/s
      outboundNetwork: 10000KB/s
    # goals: [...]
```

Use `goals` to choose optimization goals, `brokerCapacity` to change default capacity limits, and `overrides` for per-broker network limits on heterogeneous nodes.

**Checklist**

1. Define capacity limits for your nodes.
2. Choose goals deliberately.
3. Do not expect self-healing.

## Checked

2026-11-03. Confirmed in the Cruise Control section: the four components, the REST API features Strimzi uses, and that self-healing is not supported (custom JARs via a custom image).

Method: documentation only; no commands were run.
