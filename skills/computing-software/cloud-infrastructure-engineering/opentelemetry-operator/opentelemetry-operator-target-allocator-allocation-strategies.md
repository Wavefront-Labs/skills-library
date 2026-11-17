---
id: computing-software.cloud-infrastructure-engineering.opentelemetry-operator.opentelemetry-operator-target-allocator-allocation-strategies
name: opentelemetry-operator-target-allocator-allocation-strategies
category: computing-software
field: cloud-infrastructure-engineering
product: opentelemetry-operator
tags: [opentelemetry-operator, allocation-strategy, consistent-hashing, least-weighted, per-node, fallback-strategy]
level: advanced
status: docs-checked
description: "Choose between consistent-hashing, least-weighted and per-node target allocation, and configure a per-node fallback strategy for targets without a node."
sources: ["https://github.com/open-telemetry/opentelemetry-operator/blob/main/docs/target-allocator/README.md", "https://github.com/open-telemetry/opentelemetry-operator/blob/main/docs/api/opentelemetrycollectors.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Target allocation strategies

Strategies, set with `allocation_strategy` (config file) or `spec.targetAllocator.allocationStrategy`:

consistent-hashing (default). Implements consistent hashing with bounded loads. Only the target URL is hashed, so label changes do not move targets between Collectors. Assignments are stable but rebalance when the Collector count changes.

least-weighted. Assigns each target to the Collector with the fewest targets. More stable assignment when Collector count changes, at the cost of a less even distribution.

per-node. Assigns each target to the Collector running on the same Node as the target. It only makes sense with a Collector in `daemonset` mode. Warning from the docs: targets not tied to a Node, such as control plane components, are left unassigned by default.

To assign those with another strategy, configure a fallback:

```yaml
allocation_strategy: per-node
allocation_strategy_config:
  per_node:
    fallback_strategy:
      name: consistent-hashing
```

The `fallback_strategy` takes the fallback's `name` plus options keyed by strategy name like `allocation_strategy_config` itself. A fallback cannot have its own fallback, so chains are one level deep. The older top-level `allocation_fallback_strategy` key is deprecated in favour of `allocation_strategy_config.per_node.fallback_strategy`.

Replicas: the API reference says the TargetAllocator `replicas` should only be set to a value other than 1 if a strategy that allows high availability is chosen, and names `consistent-hashing` and `per-node` as the strategies that can run in a high availability mode.

## Checked

Method: docs-checked 2026-11-09 against the Target Allocator README (docs/target-allocator, read in full) and the OpenTelemetryCollector API reference (targetAllocator replicas entry). Dropped the default PodDisruptionBudget claim, which the pages read do not state.
