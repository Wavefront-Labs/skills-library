---
id: computing-software.devops-ci-cd.woodpecker-ci.woodpecker-cron-jobs
name: woodpecker-cron-jobs
category: computing-software
field: devops-ci-cd
product: woodpecker-ci
tags: [cron, schedules, scheduled-pipelines]
level: practitioner
status: docs-checked
description: "Schedule Woodpecker pipelines with cron jobs and the cron event filter."
sources:
  - https://woodpecker-ci.org/docs/usage/cron
  - https://woodpecker-ci.org/docs/usage/workflow-syntax
  - https://woodpecker-ci.org/docs/usage/secrets
  - https://woodpecker-ci.org/docs/usage/security-boundaries
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Woodpecker cron jobs

Creating a cron job requires at least push access to the repository.

1. Add the event filter to every step that should run from cron. Optionally name the job to target it:

```yaml
steps:
  - name: sync_locales
    image: weblate_sync
    settings:
      url: example.com
      token:
        from_secret: weblate_token
    when:
      event: cron
      cron: "name of the cron job"
```

2. Create the cron job in the repository settings.

The schedule syntax follows the gdgvda/cron Go library. Examples: `@every 5m`, `@daily`, `30 * * * *`.

The `cron` filter matches the job name and supports wildcards such as `sync_*`. It only applies to cron events, so keep `event: cron` in the same entry.

Cron pipelines have no author and never need approval. A secret created with the CLI default is available for `push`, `tag` and `deployment` events, not `pull_request`.

## Checked

2026-11-08. Read the Woodpecker Cron page in full, the cron filter and event list of the Workflow syntax page, the Secrets page, and the approval section of the Security boundaries page. Removed the `CI_PIPELINE_EVENT=cron` claim and the statement that secrets reach cron pipelines only when the `cron` event is enabled, which none of those pages state.

Method: documentation only; no commands were run.
