---
id: computing-software.cloud-infrastructure-engineering.hashicorp-vault.vault-database-static-roles
name: vault-database-static-roles
category: computing-software
field: cloud-infrastructure-engineering
product: hashicorp-vault
tags: [vault, static-roles, rotation-period, static-role]
level: practitioner
status: docs-checked
description: "Manage fixed database users with Vault static roles, rotation_period or rotation_schedule, and import behaviour."
sources: ["https://developer.hashicorp.com/vault/docs/secrets/databases", "https://developer.hashicorp.com/vault/api-docs/secret/databases"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Static roles keep a stable username but rotate its password on a schedule, useful for apps that cannot take dynamic users.

```sh
vault write database/static-roles/legacy-app db_name=pg username=legacy_app \
  rotation_period=24h
vault read database/static-creds/legacy-app
vault write -force database/rotate-role/legacy-app
```

Use `rotation_schedule` (cron) instead of `rotation_period` for fixed windows; set only one.

Gotchas: by default Vault rotates a static user's password as soon as it is onboarded, which breaks any app still using the old password; set `skip_import_rotation` on the role (or `skip_static_role_import_rotation` on the connection), or set the initial password, and plan the cut-over. Never assign the connection's root user to a static role: any dynamic or static users on that connection fail after the rotation. `rotation_window` can limit how long Vault has to complete a scheduled rotation. Schedule-based rotation of root credentials (`rotation_schedule` on the connection) is Enterprise.

## Checked

2026-11-03. Confirmed on the database secrets engine overview and database API pages: `static-roles/:name` with `db_name`, `username`, `rotation_period`; `static-creds/:name` returning `last_vault_rotation`; `rotate-role/:name`; `rotation_period` and `rotation_schedule` are mutually exclusive; immediate rotation on onboarding and `skip_import_rotation`; the root-user warning; Enterprise-only schedule-based root rotation. Removed: periodic-read advice, the silent-failure claim and the invented Verify step.

Method: documentation only; no commands were run.
