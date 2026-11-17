---
id: computing-software.web-development.biome.vcs-changed-since-and-staged-files
name: vcs-changed-since-and-staged-files
category: computing-software
field: web-development
product: biome
tags: [biome, changed-files, since, staged, default-branch, pre-commit, vcs-defaultbranch, incremental-check]
level: practitioner
status: docs-checked
description: "Check only changed or staged files using --changed with vcs.defaultBranch or --since, and --staged (not available in ci)."
sources:
  - https://raw.githubusercontent.com/biomejs/website/main/src/content/docs/en/configuration/integrate-with-vcs.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**Changed files (CLI only).** This feature processes only the files that changed from one revision to another. First tell Biome the default branch via `vcs.defaultBranch`:

```json
{ "vcs": { "enabled": true, "clientKind": "git", "useIgnoreFile": true, "defaultBranch": "main" } }
```

Then add `--changed`; Biome, with the help of the VCS, determines the changed files between `main` and your current revision:

```sh
biome check --changed
```

Use `--since` to specify an arbitrary branch. It takes precedence over `vcs.defaultBranch`:

```sh
biome check --changed --since=next
```

**Cautions.** Biome does not check what actually changed in the code, so even adding spaces or newlines marks a file as changed. `--changed` applies to both formatter and linter and only processes files that have diffs; it will not automatically check downstream files that import from them. After changing an exported type you might still need a full lint to catch related errors elsewhere.

**Staged files.** To check files added to the index (slated for the next commit) without running Biome on the whole project:

```sh
biome check --staged
```

The `--staged` option is not available in the `ci` command, as you are usually not expected to commit changes during CI.

## Checked

2026-11-08. Read the cited page in full (raw mdx). Unchanged: config example, both commands, --since precedence, both cautions and the ci restriction. Removed: the "usual building block for pre-commit hooks" remark and the invented Verify step, neither of which this page states.

Method: documentation only; no commands were run.
