---
id: computing-software.devops-ci-cd.renovate.semantic-commits
name: semantic-commits
category: computing-software
field: devops-ci-cd
product: renovate
tags: [semantic-commits, commit-prefix, conventional-commits, renovate]
level: intro
status: docs-checked
description: "Make Renovate commit messages and PR titles follow semantic commit conventions with semanticCommits, type and scope."
sources:
  - https://docs.renovatebot.com/semantic-commits/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Renovate autodetects whether a repository uses semantic commit prefixes by looking at the last 20 commit messages in the base branch (merge commits are ignored), and follows suit. It only recognises the conventional commits style. A configured `commitMessagePrefix` takes priority over semantic commits. You only need to configure it to override the guess.

```json
{
  "semanticCommits": "enabled",
  "semanticCommitType": "chore",
  "semanticCommitScope": "deps"
}
```

- `semanticCommits` is `auto` (default), `enabled` or `disabled`; set `enabled` or `disabled` to override autodetection. It makes most sense at repository level.
- `semanticCommitType` (default `chore`) sets the prefix; for example `ci` gives `ci(deps):`.
- `semanticCommitScope` (default `deps`) sets the scope in parentheses, producing `chore(deps): update eslint to v7.30.0`.

With `config:recommended`, production dependency types such as `dependencies` already get the `fix` prefix; a package rule can set it explicitly:

```json
{
  "packageRules": [
    {
      "matchDepTypes": ["dependencies"],
      "semanticCommitType": "fix"
    }
  ]
}
```

When semantic commits are on, the PR title and commit message gain the prefix, and `commitMessageLowerCase` (default `auto`) lowercases the titles; set it to `never` to allow uppercase. Presets exist as an alternative: `:semanticCommits`, `:semanticCommitsDisabled`, `:semanticCommitTypeAll(ci)`, `:semanticCommitScope(package)` and `:semanticCommitScopeDisabled`.

## Checked

2026-11-03. Confirmed against the Renovate Semantic Commit messages page and the configuration options page (`semanticCommits`, `semanticCommitType`, `semanticCommitScope`, `commitMessageLowerCase`). Removed: the `build` type example, the invented example title, and the claim that lowercasing satisfies linters.

Method: documentation only; no commands were run.
