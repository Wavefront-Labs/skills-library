---
id: computing-software.cloud-infrastructure-engineering.harbor.gdpr-user-deletion
name: gdpr-user-deletion
category: computing-software
field: cloud-infrastructure-engineering
product: harbor
tags: [gdpr, gdpr-delete-user, gdpr-audit-logs, user-deletion, harbor]
level: advanced
status: docs-checked
description: "Make Harbor user deletion replace usernames, emails and audit entries with checksums using GDPR_DELETE_USER and GDPR_AUDIT_LOGS."
sources:
  - https://goharbor.io/docs/main/administration/managing-users/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
By default Harbor does not remove a deleted user from its database. It marks the user as deleted and appends `#<user_id>` to the username and email address, so original values stay readable in the database and audit log.

Two settings change this:
- `GDPR_DELETE_USER` (Helm value `core.gdpr.deleteUser`): on delete, Harbor replaces the username, email address and full name with the CRC32 checksum of each value, followed by `#<user_id>`.
- `GDPR_AUDIT_LOGS` (Helm value `core.gdpr.auditLogsCompliant`): on delete, Harbor starts a job that replaces that user name in all of their audit log entries with the CRC32 checksum, in both the Audit Logs and legacy tabs.

They cannot be set in the Harbor interface or through the `/api/v2.0/configurations` API. They are read from the environment of the `core` container at startup.

- Helm chart: set `core.gdpr.deleteUser` and/or `core.gdpr.auditLogsCompliant` to `true` in `values.yaml` and upgrade the release.
- Installer: add `GDPR_DELETE_USER=true` and/or `GDPR_AUDIT_LOGS=true` to `common/config/core/env` in the installation directory, then run `docker compose up -d --force-recreate core`.

Gotcha: the settings apply only to users deleted after they are enabled. Earlier deleted users and their audit entries are unchanged. In LDAP/AD and OIDC modes, deleting a user removes only the Harbor data, not the provider account.

## Checked

- 2026-11-03: concrete claims (parameter names, defaults, steps, limits, UI labels) read against the official Harbor docs: Managing Users.
Method: documentation only; no commands were run.
