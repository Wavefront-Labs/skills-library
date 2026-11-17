---
id: computing-software.devops-ci-cd.forgejo.actions-enable-default-url-storage
name: actions-enable-default-url-storage
category: computing-software
field: devops-ci-cd
product: forgejo
tags: [actions-enabled, default-actions-url, log-retention-days, artifact-retention-days]
level: practitioner
status: docs-checked
description: "Configure the [actions] section of app.ini: enablement, default action URL, and log and artifact retention."
sources:
  - https://forgejo.org/docs/latest/admin/actions/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Forgejo does not run jobs itself; it relies on the Forgejo Runner. In app.ini:

```
[actions]
ENABLED = true
DEFAULT_ACTIONS_URL = https://data.forgejo.org
```

Actions has been enabled by default since Forgejo v1.21; set `ENABLED = false` to disable.

When `uses:` in a workflow is not an absolute URL, `DEFAULT_ACTIONS_URL` is prepended. The actions at `https://data.forgejo.org` are known to work with Forgejo Actions and are published under Free Software licences, in organizations such as `actions` (general purpose) and `docker`. If you point the setting at an instance with open registration, beware of name conflicts: `uses: foo/bar@main` will clone whatever exists at that URL plus `foo/bar`.

Storage: logs and artifacts live in Forgejo, while the cache is stored by the runner and never sent to Forgejo. Job logs expire after `LOG_RETENTION_DAYS` (default 365) and artifacts after `ARTIFACT_RETENTION_DAYS` (default 90). Their locations are set in `storage.actions_log` and `storage.artifacts`. The admin/monitor/cron page can run "Cleanup actions expired logs and artifacts" on demand.

## Checked

2026-11-04. Confirmed against the Forgejo Actions administrator guide: enabled by default since v1.21, DEFAULT_ACTIONS_URL behaviour and the name-conflict warning, log retention 365 days, artifact retention 90 days, storage sections and the cron task name. Nothing removed.

Method: documentation only; no commands were run.
