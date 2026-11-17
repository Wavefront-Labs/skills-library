---
id: computing-software.database-administration.vitess.vitess-upgrade-order-and-canary
name: vitess-upgrade-order-and-canary
category: computing-software
field: database-administration
product: vitess
tags: [upgrade, rolling-upgrade, canary, vttablet, vtgate, plannedreparentshard, semver]
level: practitioner
status: docs-checked
description: "Upgrade Vitess in the documented order: vttablet, vtctld, vtgate, then clients; canary first, roll one tablet at a time and reparent away from the primary before upgrading it."
sources:
  - https://vitess.io/docs/25.0/user-guides/operating-vitess/upgrading-vitess/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Versioning is MAJOR.MINOR.PATCH (semver). Compatibility is guaranteed across patch and minor upgrades; a major upgrade may need manual configuration changes. Always read the Upgrading section of the release notes, which overrides the default order.

Default order, bottom up: vttablet, then vtctld, then vtgate, then application code that links client libraries. All components need restarts after an upgrade.

Do it as a rolling release, usually one tablet at a time within a shard, so the others keep serving. Canary single instances, keyspaces or cells of vtgate and vttablet and let them bake for hours or days before upgrading the rest. The docs recommend automating with configuration management.

Primary tablet last: verify all replicas in the shard are upgraded, reparent away from the current primary to a replica, then upgrade the old primary.

For rolling MySQL (not Vitess) upgrades, `PlannedReparentShard` and `EmergencyReparentShard` prefer a lower-MySQL-version tablet when electing a primary, which reduces the chance of promoting a newer-version primary that older replicas cannot replicate from.

## Checked

2026-11-08. Read in full on the Upgrading Vitess page: compatibility, upgrade order, canary, rolling release, primary-last steps and the MySQL-version election note.

Method: documentation only; no commands were run.
