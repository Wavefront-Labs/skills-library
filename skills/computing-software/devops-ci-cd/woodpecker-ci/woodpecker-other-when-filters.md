---
id: computing-software.devops-ci-cd.woodpecker-ci.woodpecker-other-when-filters
name: woodpecker-other-when-filters
category: computing-software
field: devops-ci-cd
product: woodpecker-ci
tags: [ref, cron-filter, platform-filter, instance]
level: practitioner
status: docs-checked
description: "Use the ref, cron, platform, matrix and instance filters in Woodpecker `when` blocks."
sources: ["https://woodpecker-ci.org/docs/usage/workflow-syntax"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Woodpecker ref, cron, platform, matrix and instance filters

Besides branch and event, `when` supports these filters.

`ref` compares the git reference, for example tags starting with `v`:

```yaml
when:
  - event: tag
    ref: refs/tags/v*
```

`cron` filters by cron job name and only applies to cron events, so add `event: cron` as well. Wildcards work:

```yaml
when:
  - event: cron
    cron: sync_*
```

`platform` matches the agent platform, with wildcards. Use it with a matrix workflow, because a plain workflow runs on one agent with one architecture:

```yaml
when:
  - platform: [linux/*, windows/amd64]
```

`matrix` runs a step for one matrix permutation:

```yaml
when:
  - matrix:
      GO_VERSION: 1.5
      REDIS_VERSION: 2.8
```

`instance` runs a step only on the Woodpecker instance whose hostname matches:

```yaml
when:
  - instance: stage.woodpecker.company.com
```

`repo` restricts a step to a repository, such as `repo: test/test`.

Notes:

- The `cron` filter only matches cron events, so without `event: cron` it has no effect on other events.
- A plain workflow is executed by a single agent that has a single architecture, which is why `platform` is meant for matrix workflows.
- Wildcards in `platform`, such as `linux/*`, match any architecture for that operating system.

## Checked

2026-11-03. Confirmed against: workflow-syntax (ref, cron, platform, matrix, instance, repo). Removed: nothing.

Method: documentation only; no commands were run.
