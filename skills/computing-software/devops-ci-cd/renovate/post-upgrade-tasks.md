---
id: computing-software.devops-ci-cd.renovate.post-upgrade-tasks
name: post-upgrade-tasks
category: computing-software
field: devops-ci-cd
product: renovate
tags: [post-upgrade-tasks, allowed-commands, artifacts, renovate]
level: advanced
status: docs-checked
description: "Run commands after a dependency update with postUpgradeTasks, gated by the admin allowedCommands list."
sources:
  - https://docs.renovatebot.com/configuration-options/
  - https://docs.renovatebot.com/self-hosted-configuration/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`postUpgradeTasks` runs commands after Renovate updates a dependency but before the commit, so tools can regenerate files. They are blocked by default for security. The Renovate administrator must list permitted commands in the global option `allowedCommands`, a list of regexes. If the list is empty, no task runs. Each command must match at least one pattern, and with templates the final resolved command is what gets matched.

Repository config:

```json
{
  "postUpgradeTasks": {
    "commands": ["tslint --fix"],
    "fileFilters": ["yarn.lock", "**/*.js"],
    "executionMode": "update"
  }
}
```

Global config:

```json
{
  "allowedCommands": ["^tslint --fix$", "^tslint --[a-z]+$"]
}
```

- `commands` can use Handlebars templates, which are compiled before the comparison with `allowedCommands`. Do not use `git add` in commands; include new files through `fileFilters` instead.
- `fileFilters` is a list of globs for the files committed after the task runs (default `["**/*"]`, dotfiles included).
- `executionMode` is `update` (default) or `branch`: `update` runs the task for every dependency on the branch, `branch` runs it for the whole branch.
- `dataFileTemplate` writes a temporary data file whose path is in the `RENOVATE_POST_UPGRADE_COMMAND_DATA_FILE` environment variable; it is ignored if no commands are configured.
- `installTools` installs additional tools (names known to Containerbase) before the commands run.
- `allowShellExecutorForPostUpgradeCommands` (global, default `false`) runs the commands inside a shell, which has security implications because shell semantics make it difficult to restrict commands with an `allowedCommands` regex.
- `allowedUnsafeExecutions` (global) is similar to `allowedCommands` but controls implicit commands Renovate runs automatically, not those you add to `postUpgradeTasks`.

Anchor `allowedCommands` patterns with `^` and `$` as in the example. On Mend-hosted Renovate apps commands stay blocked by default, with more control depending on your plan.

## Checked

2026-11-09: read the postUpgradeTasks section (commands, dataFileTemplate, executionMode, fileFilters, installTools) of https://docs.renovatebot.com/configuration-options/ and allowedCommands, allowedUnsafeExecutions and allowShellExecutorForPostUpgradeCommands in https://docs.renovatebot.com/self-hosted-configuration/. Removed the `allowScripts` relation and the claim attributed to the security docs (that page was not read).

Method: documentation only; no commands were run.
