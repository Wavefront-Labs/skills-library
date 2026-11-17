---
id: computing-software.data-engineering.apache-nifi.connection-prioritizers
name: connection-prioritizers
category: computing-software
field: data-engineering
product: apache-nifi
tags: [data-engineering, apache-nifi, prioritizers, connections, priority-attribute, queues]
level: practitioner
status: docs-checked
description: "Queue prioritizers on a NiFi connection: default Oldest FlowFile First, FIFO, Newest First, and PriorityAttributePrioritizer where the lowest priority value goes first."
sources:
  - https://nifi.apache.org/docs/nifi-docs/html/user-guide.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Prioritizers

Prioritizers are dragged from Available to Selected prioritizers on the connection's Settings tab. Several can be selected; the one at the top of the Selected list applies first and the next breaks ties, and so on. Available prioritizers:
- OldestFlowFileFirstPrioritizer: the oldest FlowFile in the dataflow goes first. This is the default when none are selected.
- FirstInFirstOutPrioritizer: the FlowFile that reached the connection first goes first.
- NewestFlowFileFirstPrioritizer: the newest FlowFile in the dataflow goes first.
- PriorityAttributePrioritizer: extracts the `priority` attribute; the lowest value is processed first.

PriorityAttributePrioritizer details from the guide: add the attribute with UpdateAttribute before the connection; if only one FlowFile has the attribute it goes first; values may be alphanumeric ("a" before "z", "1" before "9"); if a value cannot be parsed as a long, unicode string ordering is used, so "99" precedes "100" but "A-100" precedes "A-99".

With a load balance strategy configured the connection has a queue per node plus the local queue, and the prioritizer sorts each queue independently.

Verify: with mixed `priority` values queued, List queue shows the lowest value first.

## Checked

Confirmed against the NiFi user guide section "Prioritization" and the List queue description. Removed the claim that funnels let one prioritizer apply across merged connections (the guide does not say this).

Method: docs-only read of cited pages, 2026-11-08
