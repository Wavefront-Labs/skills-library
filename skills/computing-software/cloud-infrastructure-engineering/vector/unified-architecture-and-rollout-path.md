---
id: computing-software.cloud-infrastructure-engineering.vector.unified-architecture-and-rollout-path
name: unified-architecture-and-rollout-path
category: computing-software
field: cloud-infrastructure-engineering
product: vector
tags: [unified-architecture, agent, aggregator, vector-source, vector-sink, evolution, vector]
level: practitioner
status: docs-checked
description: "Know when to add agents to an existing aggregator tier to form the unified architecture."
sources:
  - https://vector.dev/docs/setup/going-to-prod/arch/unified/
  - https://vector.dev/docs/setup/going-to-prod/architecting/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The unified architecture combines the agent and aggregator architectures into one pipeline: collect at the edge, then aggregate. The docs recommend it for teams that already run the aggregator architecture and want Vector on individual nodes. It is described as a natural evolution that hardens the pipeline in four ways:

- Agent risk drops because delivery responsibility moves from nodes to the aggregators.
- Performance improves by using Vector's native protocol through the `vector` source and sink.
- Stateless processing moves to the edge, which scales naturally.
- More sophisticated failover and disaster recovery strategies become possible.

Design guidance from the architecting document that supports it:

1. Use the best tool for the job; keep other agents where they collect unique data, for example the Datadog Agent.
2. Minimise agent responsibilities, so agents are simple forwarders and Vector carries the risk.
3. Deploy Vector close to your data and within network boundaries to avoid a single point of failure and shrink the blast radius.

Avoid one monolith aggregator. Vector is shared-nothing with no leader nodes, so deploy per network boundary and give instances the same configuration so they behave as a single logical aggregator.

Sequence: first stand up aggregators and prove them, then roll agents out one network partition at a time (see rollout-plan-blackhole-to-cutover).

## Checked

Method: docs-checked 2026-11-09 against the full Vector unified architecture page and architecting page (raw markdown from the vectordotdev/vector repo). Dropped an unsourced verification line.
