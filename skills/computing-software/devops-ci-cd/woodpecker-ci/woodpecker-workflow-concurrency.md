---
id: computing-software.devops-ci-cd.woodpecker-ci.woodpecker-workflow-concurrency
name: woodpecker-workflow-concurrency
category: computing-software
field: devops-ci-cd
product: woodpecker-ci
tags: [concurrency, deployment-lock, queue]
level: advanced
status: docs-checked
description: "Limit parallel runs of a Woodpecker workflow with the concurrency setting."
sources: ["https://woodpecker-ci.org/docs/usage/workflows", "https://woodpecker-ci.org/docs/usage/project-settings"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Woodpecker workflow concurrency

By default workflows have no concurrency limit. Use `concurrency` to cap how many instances run at once, for example for deployments. Extra instances stay queued and start when a running one finishes; nothing is cancelled.

```yaml
steps:
  - name: deploy
    image: debian:stable-slim
    commands:
      - echo deploying

concurrency:
  limit: 1
```

Shorthand: `concurrency: 1`.

Ordering: queued workflows of the same group start in the order their pipelines were created, not in the order they become ready. A later pipeline cannot overtake an earlier one that is still waiting, so deployments happen in commit order even when `depends_on` makes durations vary.

Groups: by default the limit applies per workflow within a repository. Set `group` to share a limit across workflows or make it more specific. Groups support variable substitution:

```yaml
concurrency:
  limit: 1
  group: deploy-${CI_COMMIT_BRANCH}
```

This limits deployments per branch. Compare with the project setting that cancels previous pipelines, which interrupts running work, whereas concurrency only queues.

## Checked

2026-11-03. Confirmed against: workflows (concurrency, shorthand, ordering, groups) and project-settings (cancel previous pipelines). Removed: nothing.

Method: documentation only; no commands were run.
