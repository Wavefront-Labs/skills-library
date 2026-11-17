---
id: computing-software.devops-ci-cd.renovate.base-branch-patterns
name: base-branch-patterns
category: computing-software
field: devops-ci-cd
product: renovate
tags: [base-branch-patterns, release-branches, use-base-branch-config, renovate]
level: advanced
status: docs-checked
description: "Make Renovate update branches other than the default using baseBranchPatterns and useBaseBranchConfig."
sources:
  - https://docs.renovatebot.com/configuration-options/#basebranchpatterns
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

By default Renovate processes only the repository's default branch. `baseBranchPatterns` (formerly `baseBranches`) lets it also or instead process others, for example a `dev` branch, or multiple release streams.

```json
{
  "baseBranchPatterns": ["main", "next", "/^release\\/.*/"]
}
```

Details:

- Entries may be exact names or regex patterns written with slashes, so you can follow a family of release branches.
- Prefix a regex with `!` to negate it (use a single negation and do not mix it with other names), or use the special string `$default` for the repository's default branch.
- The configuration still comes from the default branch, not from each base branch. Set `useBaseBranchConfig` to `merge` to merge each base branch's config file over the default branch config. The file name must match the default branch's and cannot be `package.json`.

Do not use `baseBranchPatterns` when you have set a `forkToken`. A package rule can target specific branches with `matchBaseBranches`. The `useBaseBranchConfig=merge` setting is useful for testing config changes in base branches.

## Checked

2026-11-03. Confirmed against the Renovate configuration options page: `baseBranchPatterns` (former name, default, exact and regex entries, negation, `$default`, `forkToken` note), `useBaseBranchConfig` and `matchBaseBranches`. Removed unsupported cautions about PR and CI multiplication, `prConcurrentLimit`, automerge on release branches, and testing config edits.

Method: documentation only; no commands were run.
