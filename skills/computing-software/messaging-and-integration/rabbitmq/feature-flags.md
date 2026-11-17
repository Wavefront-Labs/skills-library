---
id: computing-software.messaging-and-integration.rabbitmq.feature-flags
name: feature-flags
category: computing-software
field: messaging-and-integration
product: rabbitmq
tags: [rabbitmq, messaging, feature-flags]
level: advanced
status: docs-checked
description: "Manage feature flags to enable new capabilities across mixed-version clusters."
sources:
  - https://www.rabbitmq.com/docs/feature-flags
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Feature flags

**Goal:** Control version-dependent features.

## Steps
1. `rabbitmqctl list_feature_flags`; `rabbitmqctl enable_feature_flag <all | name>` (also under Admin > Feature flags in the management UI).
2. When a node starts for the first time, all stable feature flags are enabled by default; after an upgrade, new flags are left disabled until you enable them.
3. Enable flags only after every node runs the new version. Once enabled, a flag cannot be disabled.

## Failure modes
- A node can join or re-join a cluster only if it supports every flag enabled in the cluster, and the cluster supports every flag enabled on that node.

## Verify
- `rabbitmqctl list_feature_flags` shows the flags enabled.

## Checked

2026-11-02. Confirmed in docs/feature-flags: list and enable commands, defaults on first start and after upgrade, join rule, irreversibility. Removed: the "unconfirmed per release" auto-enable line (replaced by the documented behaviour).
Method: documentation only; no commands were run.
