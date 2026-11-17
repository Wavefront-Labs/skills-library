---
id: computing-software.devops-ci-cd.backstage.catalog-github-discovery
name: catalog-github-discovery
category: computing-software
field: devops-ci-cd
product: backstage
tags: [github-discovery, catalog-providers, catalog-path, backstage]
level: practitioner
status: docs-checked
description: "Auto-register catalog-info.yaml files across a GitHub organisation with the catalog GitHub provider and webhook events."
sources:
  - https://backstage.io/docs/integrations/github/discovery
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Install the GitHub catalog module and configure a provider so repositories are scanned for descriptors.

```bash
yarn --cwd packages/backend add @backstage/plugin-catalog-backend-module-github
```

```ts
backend.add(import('@backstage/plugin-catalog-backend-module-github'));
```

```yaml
catalog:
  providers:
    github:
      providerId:
        organization: 'example-org'
        catalogPath: '/catalog-info.yaml'
        filters:
          branch: 'main'
          repository: '.*'
        schedule:
          frequency: { minutes: 30 }
          timeout: { minutes: 3 }
```

- The provider id can be any camelCase string.
- `catalogPath` is the file looked up in each repository.
- `filters.branch` and `filters.repository` (a regex) narrow the search.
- `filters.branch` defaults to the repository default branch and cannot contain a slash; optional `topic` filters take `include` and `exclude` lists.
- `schedule` takes the same options as `SchedulerServiceTaskScheduleDefinition`.

For faster updates than polling, add events support: install `@backstage/plugin-events-backend-module-github`, configure a GitHub webhook, and set `events.modules.github.webhookSecret`. Events can arrive through an HTTP endpoint (`events.http.topics` containing `github`) or an AWS SQS module.

## Checked

2026-11-03. Confirmed on the GitHub Discovery page: the module package and `backend.add` line, the `catalog.providers.github` block with `catalogPath`, `filters.branch` and `filters.repository` (regex), `schedule`, that the provider id can be any camelCase string, the events module `@backstage/plugin-events-backend-module-github`, `events.modules.github.webhookSecret`, the HTTP topic `github` and the AWS SQS alternative. Removed: the statement about `integrations.github` credentials and the "safety net" sentence, which this page does not state. Tightened the schedule bullet to what the page says.

Method: documentation only; no commands were run.
