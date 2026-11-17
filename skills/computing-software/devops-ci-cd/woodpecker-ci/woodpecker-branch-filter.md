---
id: computing-software.devops-ci-cd.woodpecker-ci.woodpecker-branch-filter
name: woodpecker-branch-filter
category: computing-software
field: devops-ci-cd
product: woodpecker-ci
tags: [branch, glob, doublestar]
level: practitioner
status: docs-checked
description: "Filter Woodpecker steps by branch with lists, globs and include/exclude rules."
sources: ["https://woodpecker-ci.org/docs/usage/workflow-syntax"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Woodpecker branch filter

The `branch` condition accepts a single value, a list, a glob, or an include/exclude map.

```yaml
when:
  - branch: [main, develop]
```

```yaml
when:
  - branch: prefix/*
```

```yaml
when:
  - branch:
      include: [main, release/*]
      exclude: [release/1.0.0, release/1.1.*]
```

Matching uses the doublestar library. A pattern that starts with `*` must be quoted in YAML, and a literal `/` needs escaping. The documented examples:

- `*\\/*` matches names with exactly one `/`
- `*\\/**` matches names with at least one `/`
- `*` matches names without `/`
- `**` matches everything

Things to remember:

- Branch conditions are not applied to tag events.
- A step with `branch: main` also triggers for pull requests whose target branch is `main`.
- Add an `event: push` condition to limit it to pushes on `main` only.

## Checked

2026-11-08. Read the Woodpecker workflow syntax page in full (raw markdown) and confirmed the branch condition forms, doublestar matching, quoting and escaping note, the four pattern examples, no branch conditions on tags, and pull request target-branch behaviour. Removed: the claim that CI_COMMIT_BRANCH equals the target branch for pull requests, which the page does not state.

Method: documentation only; no commands were run.
