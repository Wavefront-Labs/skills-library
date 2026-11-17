---
id: computing-software.devops-ci-cd.backstage.search-collators
name: search-collators
category: computing-software
field: devops-ci-cd
product: backstage
tags: [catalog-collator, techdocs-collator, collator-schedule, backstage]
level: practitioner
status: docs-checked
description: "Index catalog entities and TechDocs pages by installing collator modules and tuning schedule and filter."
sources:
  - https://backstage.io/docs/features/search/collators
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Collators feed documents to the index. Install the module, add it to the backend, then tune it under `search.collators`.

```bash
yarn --cwd packages/backend add @backstage/plugin-search-backend-module-catalog
```

```ts
backend.add(import('@backstage/plugin-search-backend-module-catalog'));
```

```yaml
search:
  collators:
    catalog:
      schedule:
        initialDelay: { seconds: 90 }
        frequency: { hours: 6 }
        timeout: { minutes: 3 }
      filter:
        kind: ['component', 'api']
        spec.lifecycle: production
```

- `schedule` uses the scheduler task definition: `initialDelay`, `frequency` and `timeout`; `initialDelay` and `frequency` accept cron, ISO duration or human duration values, `timeout` accepts ISO or human duration.
- `filter` restricts which entities are indexed, for example by kind and `spec.lifecycle`.
- The TechDocs collator is added with `@backstage/plugin-search-backend-module-techdocs` and has its own entry under `search.collators`.

`filter` uses the `EntityFilterQuery` syntax: keys in one object are AND-ed and a list of objects is OR-ed. The TechDocs collator by default only reads catalog entities that have the `backstage.io/techdocs-ref` annotation.

## Checked

2026-11-03. Confirmed against the Backstage Search Collators page: module names, `search.collators` schedule keys, catalog `filter` example and semantics, TechDocs collator module. Removed: unsupported advice on frequency load, restarts and timeout sizing.

Method: documentation only; no commands were run.
