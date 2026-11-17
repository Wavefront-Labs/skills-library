---
id: computing-software.devops-ci-cd.renovate.self-hosted-dry-run
name: self-hosted-dry-run
category: computing-software
field: devops-ci-cd
product: renovate
tags: [dry-run, extract, lookup, renovate]
level: intro
status: docs-checked
description: "Preview Renovate behaviour without changing repositories using dryRun extract, lookup and full."
sources:
  - https://docs.renovatebot.com/self-hosted-configuration/#dryrun
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Set the global `dryRun` option to preview Renovate's behaviour in logs without changing repository files. The information appears mainly at debug log level.

Values:

- `null`: the default; a normal run that creates, updates and deletes branches and PRs.
- `"extract"`: a very quick package file scan that identifies the extracted dependencies.
- `"lookup"`: a package file scan that identifies extracted dependencies and the updates available.
- `"full"`: a dry run that logs messages instead of creating, updating or deleting branches and PRs.

```json
{
  "dryRun": "lookup"
}
```

## Checked

2026-11-08: read the `dryRun` section of the Self-Hosted Configuration page (raw source of docs.renovatebot.com/self-hosted-configuration; partial read, other sections not read for this skill). Confirmed the four `dryRun` values and that information appears mainly at debug log level. Removed the `--dry-run` CLI claim, the `LOG_LEVEL` command, and the `managerFilePatterns`, `hostRules`, `renovate-config-validator` and narrow-filter advice, which the section does not state.
Method: documentation only; no commands were run.
