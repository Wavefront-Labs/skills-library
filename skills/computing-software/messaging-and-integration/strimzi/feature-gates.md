---
id: computing-software.messaging-and-integration.strimzi.feature-gates
name: feature-gates
category: computing-software
field: messaging-and-integration
product: strimzi
tags: [feature-gates, strimzi-feature-gates, alpha-beta-ga]
level: advanced
status: docs-checked
description: "Enable or disable Strimzi operator features with STRIMZI_FEATURE_GATES."
sources: ["https://strimzi.io/docs/operators/latest/deploying.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Feature gates

**Goal:** trial features safely using operator feature gates.

Feature gates enable or disable specific operator features. They have three maturity stages:

- **Alpha:** disabled by default; experimental or unstable, possibly not production-ready.
- **Beta:** enabled by default but can be disabled; well tested.
- **GA:** always enabled and cannot be disabled.

Gates apply to all Strimzi operators; one operator may ignore a gate another uses, but it can still be configured on all of them.

Set them with the `STRIMZI_FEATURE_GATES` environment variable on the operator. Use a comma-separated list; `+` enables and `-` disables:

```yaml
env:
  - name: STRIMZI_FEATURE_GATES
    value: +FeatureGate1,-FeatureGate2
```

When the User Operator and Topic Operator are deployed through the `Kafka` resource, the Cluster Operator propagates the gate configuration automatically. When they are deployed **standalone**, with no Cluster Operator to configure them, set the variable directly in their Deployments.

**Checklist**

1. Check the stage of a gate before enabling it.
2. Do not try to disable a GA gate.
3. Set gates on standalone Topic and User Operators yourself.

## Checked

2026-11-03. Confirmed in Feature gates: alpha/beta/GA stages, applicability to all operators, STRIMZI_FEATURE_GATES +/- syntax, and propagation to Topic/User Operators unless standalone.

Method: documentation only; no commands were run.
