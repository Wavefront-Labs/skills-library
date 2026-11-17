---
id: computing-software.cloud-infrastructure-engineering.calico.whisker-flow-log-fields-and-goldmane-api
name: whisker-flow-log-fields-and-goldmane-api
category: computing-software
field: cloud-infrastructure-engineering
product: calico
tags: [flow-logs, whisker, goldmane, grpc, policies, reporter, aggregation, observability]
level: practitioner
status: docs-checked
description: "Read a Calico flow log: how logs aggregate, the main fields (action, reporter, bytes, packets, labels, policies) and the Goldmane gRPC API."
sources:
  - https://docs.tigera.io/calico/latest/observability/view-flow-logs
  - https://docs.tigera.io/calico/latest/observability/enable-whisker
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A flow log aggregates connections that match the same criteria (source, destination, policies) over a period. Roughly 1000 connections in a minute might become about 15 flow logs, each a distinct kind of connection. Uses named by the page: network visibility, troubleshooting (is traffic denied by policy or reaching the destination), security review, and validating policy, especially staged policies before enforcement.

Main fields:

| Field | Meaning |
|---|---|
| `start_time`, `end_time` | Collection window, Unix timestamp |
| `action` | `allow` or `deny` |
| `reporter` | `src` (initiator side) or `dst` (receiver side) |
| `source_name`, `dest_name` | Pod name, or the aggregated name; non-pod endpoints differ |
| `source_namespace`, `dest_namespace` | `-` means not namespaced |
| `dest_port` | Not applicable to ICMP |
| `source_labels`, `dest_labels` | Pod labels; a hyphen indicates aggregation |
| `protocol` | Protocol |
| `bytes_in`, `bytes_out`, `packets_in`, `packets_out` | Counts in the window |
| `policies` | Policies that interacted with the flow |

In Whisker you can filter the live stream by policy, namespace, pod or other criteria.

**Scripting.** Goldmane, the flow logs API, makes the aggregated logs available as a gRPC API and can be used without Whisker. The page links to a Flow logs API page for use in your own scripts.

## Checked

Read in full on 2026-11-08: the View flow logs page and the Enable the flow logs API and Calico Whisker page. Aggregation behaviour and the listed fields match the first; the gRPC description matches the second. Some fields in the page table are omitted here, and a claim about the separate Flow logs API page was removed as that page was not read.

Method: documentation only; no commands were run.
