---
id: computing-software.devops-ci-cd.woodpecker-ci.woodpecker-path-filter
name: woodpecker-path-filter
category: computing-software
field: devops-ci-cd
product: woodpecker-ci
tags: [path, monorepo, changed-files]
level: advanced
status: docs-checked
description: "Run Woodpecker steps only when certain files changed, using the path filter."
sources: ["https://woodpecker-ci.org/docs/usage/workflow-syntax", "https://woodpecker-ci.org/docs/usage/environment"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Woodpecker path filter

The `path` condition runs a step only when files matching a glob changed. It applies only to `push` and `pull_request` events.

```yaml
when:
  - path: 'src/*'
```

Use `include` and `exclude` lists of doublestar glob patterns:

```yaml
when:
  - path:
      include: ['.woodpecker/*.yaml', '*.ini']
      exclude: ['*.md', 'docs/**']
      ignore_message: '[ALL]'
      on_empty: true
```

Details:

- `pull_request` events contain all files changed in the pull request, not just those of the last pushed commit.
- For pipelines without file changes (empty commits), `on_empty` decides whether the condition is true. The default is true.
- If the commit message contains the `ignore_message` string, such as `[ALL]`, all path conditions and `on_empty` are ignored, so everything runs.
- The list of changed files is exposed as `CI_PIPELINE_FILES`; it is empty for other events and undefined if more than 500 files were touched.

In a monorepo, path filters on whole workflows can leave a deploy workflow blocked on a dependency that never ran. Mark such dependencies `optional: true` (see the workflows page).

## Checked

2026-11-03. Confirmed against: workflow-syntax (path, include/exclude, ignore_message, on_empty) and environment (CI_PIPELINE_FILES, 500 files). Removed: the Bitbucket Cloud pull request claim (the forge matrix lists when.path as supported on every forge).

Method: documentation only; no commands were run.
