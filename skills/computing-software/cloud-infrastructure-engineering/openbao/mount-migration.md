---
id: computing-software.cloud-infrastructure-engineering.openbao.mount-migration
name: mount-migration
category: computing-software
field: cloud-infrastructure-engineering
product: openbao
tags: [openbao, mount-migration, remount, namespaces, leases]
level: advanced
status: docs-checked
description: "Move OpenBao secrets or auth mounts with sys/remount: async migration IDs, namespace limits, lease revocation and alias cleanup."
sources:
  - https://raw.githubusercontent.com/openbao/openbao/main/website/content/docs/concepts/mount-migration.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Mount migration

- `sys/remount` starts a migration. It is asynchronous and returns a migration ID.
- `sys/remount/status` checks progress with that ID.

## What moves

Secrets and auth mounts, within or across namespaces. Configuration carries over (database roles, userpass users stay available). Rate limit and lease count quotas are updated to the new path.

## Restrictions

Source and destination must be the namespace where `/sys/remount` is called or its children. Path filters are respected, so availability on secondary clusters can change.

## Warnings

- Existing leases on the mount are revoked, including dynamic secrets and auth tokens. Mounts with many leases can take a long time.
- Cross-namespace moves leave aliases pointing at an invalid mount. Remove them in the source namespace and create equivalent entities and aliases in the target, or let OpenBao generate them at login.
- Policies referencing moved paths may break; update them or create equivalent mounts in the target namespace.

## Checked

2026-11-04. Confirmed against the Mount migration page: asynchronous sys/remount with a migration ID and sys/remount/status, namespace restrictions, configuration carried over, quota updates, path filters, lease revocation, alias cleanup after cross-namespace moves and policy updates. Removed an unsupported closing advice sentence about client credential expiry.

Method: documentation only; no commands were run.
