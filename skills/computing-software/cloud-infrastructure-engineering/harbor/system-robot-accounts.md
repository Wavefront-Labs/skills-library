---
id: computing-software.cloud-infrastructure-engineering.harbor.system-robot-accounts
name: system-robot-accounts
category: computing-software
field: cloud-infrastructure-engineering
product: harbor
tags: [robot-account, system-robot, robot-prefix, robot-token-expiration, harbor]
level: practitioner
status: docs-checked
description: "Create and manage Harbor system robot accounts: scope, expiry (default 30 days), name prefix, secret refresh and docker login."
sources:
  - https://goharbor.io/docs/main/administration/robot-accounts/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
System robot accounts give non-user credentials across many projects, each with system permissions and per-project permissions. They work through OCI clients and the Harbor API but cannot log in to the UI. Project-scoped robots are covered separately.

Create one as a system administrator: Administration, **Robot Accounts**, **New Robot Account**:
1. Name and optional description.
2. Expiration: defaults to the system setting, or choose **Never Expired**.
3. Select system permissions.
4. Tick **Cover all projects** to include every existing and future project, or pick projects and per-project permissions in the table (the **Reset All Project Permissions** dropdown changes every project, not just the visible page).
5. **FINISH**, then **Export to File** or copy the secret.

Harbor does not store secrets, so you cannot retrieve the secret later. Use **Action**, **Refresh Secret** for a random or manually entered new secret. Other actions are Edit, Deactivate and Delete.

Settings (Configuration, System Settings):
- **Robot Token Expiration (Days)**: default 30, applies to all robots in all projects.
- **Robot Name Prefix**: default `robot$`. The full name is `<prefix><account_name>`. Changes apply to existing and future robots except those created in v2.1 and earlier.

Authenticate with `docker login <harbor_address>`, username `<prefix><account_name>`, password the secret.

## Checked

- 2026-11-03: concrete claims (parameter names, defaults, steps, limits, UI labels) read against the official Harbor docs: Create System Robot Accounts.
Method: documentation only; no commands were run.
