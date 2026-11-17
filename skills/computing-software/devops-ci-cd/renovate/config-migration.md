---
id: computing-software.devops-ci-cd.renovate.config-migration
name: config-migration
category: computing-software
field: devops-ci-cd
product: renovate
tags: [config-migration, migration-pr, legacy-config, renovate]
level: practitioner
status: docs-checked
description: "Keep Renovate config current with configMigration pull requests and understand the silent internal migration."
sources:
  - https://docs.renovatebot.com/config-migration/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

When maintainers rename, remove or combine options, they add migration code so legacy configs keep working. Renovate migrates the config internally before using it, and the only visible sign is a debug log message showing the old and new config. Legacy config therefore works indefinitely.

Even so, the docs recommend updating names regularly because current names are easier to understand, find in the docs, and debug with maintainers.

Enable automatic migration pull requests:

```json
{
  "configMigration": true
}
```

Config migration PRs are disabled by default. When on, Renovate opens a PR updating your config file to current names, and the dependency dashboard links it.

Related points:

- `renovate-config-validator --strict` fails if the config still needs migration, so you can enforce this in CI.
- If migration is needed but PRs are disabled, Renovate adds a checkbox to the Dependency Dashboard; ticking it creates the migration PR on demand. The same applies when a previous migration PR was closed.
- `configWarningReuseIssue` controls whether Renovate reuses one issue for config warnings rather than opening new ones.


## Checked

2026-11-03. Confirmed against the Renovate Config Migration page (silent internal migration, `configMigration`, disabled by default, dashboard link and on-demand checkbox), the Config Validation page (`--strict`) and the configuration options page (`configWarningReuseIssue`). Removed: `migratePresets` (not on these pages) and the unsupported advice about formatting loss.

Method: documentation only; no commands were run.
