---
id: computing-software.database-administration.cloudnative-pg.operator-upgrade-two-step-rollout-control
name: operator-upgrade-two-step-rollout-control
category: computing-software
field: database-administration
product: cloudnative-pg
tags: [upgrade, operator, instance-manager, primaryupdatestrategy, rollout-delay, in-place, switchover]
level: practitioner
status: docs-checked
description: "Upgrade the operator knowing it rolls every cluster: primaryUpdateStrategy, staggering with CLUSTERS_ROLLOUT_DELAY and INSTANCES_ROLLOUT_DELAY, and in-place updates."
sources:
  - https://github.com/cloudnative-pg/cloudnative-pg/blob/main/docs/src/installation_upgrade.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Upgrading is two steps: (1) upgrade the controller and its resources (apply the newer manifest, or use your distribution's package manager); (2) upgrade the instance manager in every PostgreSQL pod, triggered automatically afterwards. Read the release notes first, as some versions need extra steps, and upgrade sequentially if you cannot keep pace with the roughly monthly releases.

By default step 2 is a rolling update of each cluster, one instance at a time, ending in a switchover governed by `primaryUpdateStrategy`. `unsupervised` (default) switches over automatically, so applications must reconnect; with `supervised` you promote the new primary with the `cnpg` plugin. A single-instance cluster is simply restarted, because `supervised` is not supported there.

All clusters roll out at once by default. Stagger them with operator options:

- `CLUSTERS_ROLLOUT_DELAY`: seconds between different clusters (default `0`).
- `INSTANCES_ROLLOUT_DELAY`: seconds between instances of one cluster (default `0`).

To avoid restarting PostgreSQL, set `ENABLE_INSTANCE_MANAGER_INPLACE_UPDATES` to `'true'` in the operator configuration. The new instance manager binary replaces the old one after an integrity check and adopts the running postmaster, so no switchover occurs. The trade-off: the Pod changes after start, and its init container image no longer reflects the operator version.

Within API version v1 (operator 1.x.y) each release is compatible with the previous. When versions are not directly upgradable, remove the old operator first; user data is untouched.

## Checked

2026-11-04. Two-step upgrade, rollout delay variables, in-place update variable and version-compatibility rules confirmed on the Installation and upgrades page.

Method: documentation only; no commands were run.
