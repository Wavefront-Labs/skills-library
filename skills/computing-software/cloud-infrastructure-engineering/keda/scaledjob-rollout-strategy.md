---
id: computing-software.cloud-infrastructure-engineering.keda.scaledjob-rollout-strategy
name: scaledjob-rollout-strategy
category: computing-software
field: cloud-infrastructure-engineering
product: keda
tags: [rollout-strategy, gradual, propagationpolicy, scaledjob-update, foreground-deletion]
level: advanced
status: docs-checked
description: "Choose how a ScaledJob update treats running Jobs: default termination versus gradual rollout, and the foreground or background propagation policy."
sources:
  - https://keda.sh/docs/2.17/reference/scaledjob-spec/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
When you edit an existing ScaledJob, KEDA must decide what to do with Jobs created from the old spec. The `spec.rollout` section controls this.

`rollout.strategy` accepts `default` (the default) or `gradual`:
- `default`: KEDA terminates existing Jobs whenever the ScaledJob is updated, then recreates them with the latest specification. This can interrupt in-flight work.
- `gradual`: KEDA does not delete existing Jobs. Only new Jobs are created with the updated spec, so running work finishes on the old definition.

`rollout.propagationPolicy` applies to the `default` strategy and defaults to `background`, the Kubernetes background cascading deletion. Set it to `foreground` to change this; see the Kubernetes documentation for the semantics.

The older top-level `rolloutStrategy` field still appears in the specification but is marked deprecated; use `rollout.strategy`.

## Checked

2026-11-03. Confirmed on the 2.17 ScaledJob specification: rollout.strategy, propagationPolicy, deprecated rolloutStrategy. Removed: a practical-choice recommendation and a foreground-deletion explanation the page does not give.

Method: documentation only; no commands were run.
