---
id: computing-software.cloud-infrastructure-engineering.vector.agent-architecture
name: agent-architecture
category: computing-software
field: cloud-infrastructure-engineering
product: vector
tags: [agent, architecture, edge, stateless-processing, memory-buffers, deployment, vector]
level: practitioner
status: docs-checked
description: "Deploy Vector as a per-node agent with fast, stateless processing and in-memory buffering."
sources:
  - https://vector.dev/docs/setup/going-to-prod/arch/agent/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The agent architecture runs Vector on every node for local collection and processing. Vector can collect directly, indirectly through another agent, or both, and processing can happen locally or in an aggregator.

Use it for simple environments that do not need high durability or availability, for fast stateless work that does not hold data for long (merging multi-line logs, aggregating host-specific metrics), and when operators can change nodes without much friction. Otherwise prefer the aggregator or unified architecture.

Docs guidance:

- Replace only agents doing generic data forwarding; integrate with every other agent.
- Limit processing to fast, stateless operations and delivery to fast, streaming delivery. Long-lived batching belongs on aggregators.
- Buffer in memory, not on disk. Durability needs push you to the aggregator architecture.
- Cap the agent at 2 vCPUs and 4 GiB of memory; if it needs more, move heavy processing to aggregators.
- Mitigate failure with end-to-end acknowledgements and routing of dropped events. If one agent failing is unacceptable, use aggregators.
- Roll out one network partition and one system at a time.

Working with other agents: deploy Vector alongside agents that integrate with specific systems and produce unique data; otherwise let Vector replace them. As a rule of thumb agents should not hold data.

## Checked

Method: docs-checked 2026-11-09 against the full Vector agent architecture page (raw markdown from the vectordotdev/vector repo). Dropped an unsourced DaemonSet resource-limit check line.
