---
id: computing-software.database-administration.dragonfly.acl-file-persistence
name: acl-file-persistence
category: computing-software
field: database-administration
product: dragonfly
tags: [aclfile, acl-save, acl-load, acl-persistence, dragonfly]
level: practitioner
status: docs-checked
description: "Persist Dragonfly ACL users in a file with --aclfile and ACL SAVE, and place the file where Dragonfly can write it."
sources:
  - https://raw.githubusercontent.com/dragonflydb/documentation/main/docs/managing-dragonfly/acl.md
  - https://raw.githubusercontent.com/dragonflydb/documentation/main/docs/managing-dragonfly/operator/dragonfly-configuration.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
User definitions and permissions can be stored in a file. Use `--aclfile` to name the file Dragonfly loads ACL state from at startup (default empty).

Runtime changes are persisted with `ACL SAVE`, which writes the current ACL state to the `--aclfile` file.

Cautions from the docs:

- The aclfile is Redis-compatible, but the page states it must not contain key or pub/sub rules because those were not supported there; strip them if migrating a Redis file.
- For `ACL SAVE` to work the file must be writable. Do not place it under `/etc`, which is usually read-only to Dragonfly. The docs suggest `/var/lib/dragonfly/` instead, and mention editing the systemd unit file (`/lib/systemd/system/dragonfly.service`) to change that behaviour.

Operator: the Dragonfly custom resource field `aclFromSecret` (since operator v1.1.1) passes an ACL file from a Kubernetes Secret to the container.

Steps:

1. Create the file and set `--aclfile=/path/to/aclfile`.
2. Start Dragonfly and confirm users with `ACL LIST`.
3. After changes run `ACL SAVE`.
4. Restart to confirm users are reloaded.

## Checked

2026-11-04. Confirmed in the Dragonfly ACL guide (Persistence section: `--aclfile`, `ACL SAVE`, Redis compatibility, `/etc` caution, systemd unit path, `/var/lib/dragonfly/`), the flags page (`aclfile` default empty) and the Operator configuration page (`aclFromSecret`, since v1.1.1). Nothing removed.

Method: documentation only; no commands were run.
