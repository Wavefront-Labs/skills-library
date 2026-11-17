---
id: computing-software.software-engineering.pnpm.update-github-actions-changeset
name: update-github-actions-changeset
category: computing-software
field: software-engineering
product: pnpm
tags: [github-actions-update, include-github-actions, update-changeset, update-patches, registry-revisions, trust-policy-flags]
level: advanced
status: docs-checked
description: "Use pnpm update beyond npm ranges: pin GitHub Actions to commit hashes, write changesets automatically, refresh registry revisions with --patches, and per-run trust-policy flags."
sources:
  - https://pnpm.io/cli/update
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
GitHub Actions (opt-in):

```sh
pnpm outdated --include-github-actions
pnpm update --include-github-actions
```

or set `update.githubActions: true` in `pnpm-workspace.yaml`. Updated actions are pinned to exact commit hashes with the release tag kept in a comment (`uses: actions/checkout@<sha> # v5.0.0`). Local `./` actions are followed in-repo. Checks run `git ls-remote` per repository; unreadable (private) ones are skipped with a warning. For GitHub Enterprise Server set `update.githubActionsServer`.

Changesets: `pnpm update --changeset` writes a changesets-compatible `.changeset/*.md` with a `patch` bump for each workspace package whose `dependencies` or `optionalDependencies` changed (and `major` for changed `peerDependencies`). Private, unnamed and `ignore`d packages are skipped; with no `.changeset/config.json` it only warns. Default on with `update.changeset: true`; `--no-changeset` overrides.

`--patches` (v12.0.0): refresh registry revisions for the same `name@version`, rewriting lockfile integrity and revision metadata. Cannot combine with selectors, `--latest`, `--interactive` or `--global` (`ERR_PNPM_PATCHES_WITH_SELECTOR`).

Since v12.3.0 update accepts `--trust-policy`, `--trust-policy-exclude`, `--trust-policy-ignore-after`, `--trust-lockfile` per run.

## Checked

2026-11-04. Confirmed the GitHub Actions opt-in, pinning and git ls-remote behaviour, --changeset rules, --patches (v12.0.0) and ERR_PNPM_PATCHES_WITH_SELECTOR, and the v12.3.0 trust-policy flags against pnpm.io/cli/update. Removed the unsourced closing Check line.

Method: documentation only; no commands were run.
