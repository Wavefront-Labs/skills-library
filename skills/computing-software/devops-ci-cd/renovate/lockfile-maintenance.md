---
id: computing-software.devops-ci-cd.renovate.lockfile-maintenance
name: lockfile-maintenance
category: computing-software
field: devops-ci-cd
product: renovate
tags: [lock-file-maintenance, lockfile, refresh, renovate]
level: practitioner
status: docs-checked
description: "Refresh lock files on a schedule with lockFileMaintenance without changing declared dependency ranges."
sources:
  - https://docs.renovatebot.com/configuration-options/#lockfilemaintenance
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`lockFileMaintenance` deletes the lock file and lets the package manager regenerate it, so all resolved versions move to the newest ones matching your declared constraints. Renovate commits the new lock file to a branch and opens a PR. Package file ranges are untouched.

It is disabled by default:

```json
{
  "lockFileMaintenance": {
    "enabled": true,
    "automerge": true
  }
}
```

Defaults and tips:

- To keep noise low, Renovate runs it `before 4am on monday`, giving once-a-week semantics. Override with `schedule` inside the object.
- Automerge is the lowest-risk automerge candidate, because it only refreshes resolved versions within existing ranges.
- Supported lock files depend on the manager; the docs include a table, and new ones can be requested.
- The defaults of the object also set `recreateWhen` to `always`, `branchTopic` to `lock-file-maintenance` and `commitMessageAction` to `Lock file maintenance`.

Combine it with a range strategy of `update-lockfile` so in-range updates only touch the lock file. That strategy works for bundler, cargo, composer, gleam, npm, yarn, pnpm, terraform, poetry and uv.

## Checked

2026-11-03. Confirmed against the Renovate configuration options page (`lockFileMaintenance` defaults and behaviour, supported lock files table, the `rangeStrategy` `update-lockfile` manager list) and the Automerge key-concepts page (lowest-risk automerge candidate). Removed the claim that the object takes labels and the advice about a modest schedule.

Method: documentation only; no commands were run.
