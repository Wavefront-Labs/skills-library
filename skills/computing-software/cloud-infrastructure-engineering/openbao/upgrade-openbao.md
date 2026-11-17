---
id: computing-software.cloud-infrastructure-engineering.openbao.upgrade-openbao
name: upgrade-openbao
category: computing-software
field: cloud-infrastructure-engineering
product: openbao
tags: [openbao, upgrade, backup, downgrade, version-notes]
level: practitioner
status: docs-checked
description: "Upgrade OpenBao safely: back up first, replace the binary, shut down with SIGINT or SIGTERM, read every version note and test on a snapshot."
sources:
  - https://raw.githubusercontent.com/openbao/openbao/main/website/content/docs/guides/upgrade/index.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Upgrading OpenBao

## Non-HA steps

1. Back up your data first.
2. Replace the binary with the new version and restart. Automatic upgrade tasks run when OpenBao is unsealed.
3. Always stop OpenBao with `SIGINT` or `SIGTERM`.

HA ordering is on a separate page (HA upgrades); this page does not specify it.

## Rules

- Large jumps are supported, but read the upgrade notes for every version between yours and the target; they may need config changes before, during or after.
- Downgrading is not clean: swapping the old binary back is not enough. You must also roll back the data store.

## Test first

Load a snapshot of your data into a test cluster. If the cluster issues secrets to third-party resources, block external network access in the test so it cannot revoke live cloud or database credentials.

## Agent

OpenBao Agent is an API client and can lag the server version. Keep instances on the latest minor version where possible. API breaks are announced in the upgrade guide after a long deprecation period.

## Checked

2026-11-04. Read the OpenBao upgrade guide overview page in full. Confirmed: back up first, no backward compatibility guarantee for the data store, rollback needs the data store too, large jumps with per-version notes, non-HA steps, `SIGINT` or `SIGTERM`, the testing advice and the Agent note. Removed: nothing.
Method: documentation only; no commands were run.
