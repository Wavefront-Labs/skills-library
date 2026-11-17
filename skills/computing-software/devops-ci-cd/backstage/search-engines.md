---
id: computing-software.devops-ci-cd.backstage.search-engines
name: search-engines
category: computing-software
field: devops-ci-cd
product: backstage
tags: [search-engine, lunr, postgres-search, backstage]
level: practitioner
status: docs-checked
description: "Choose and configure a Backstage Search engine: Lunr for development, Postgres or Elasticsearch for production."
sources:
  - https://backstage.io/docs/features/search/search-engines
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Backstage supports three engines by default.

Lunr is an in-memory engine built into the search backend. It is enabled by default and needs only:

```ts
backend.add(import('@backstage/plugin-search-backend'));
```

The docs say Lunr suits local development and is highly discouraged in production.

Postgres reuses the database Backstage already uses, so it avoids running another service, and performs well with tens of thousands of indexed documents (the page says `ten thousands`). It requires at least Postgres 12.

```bash
yarn --cwd packages/backend add @backstage/plugin-search-backend-module-pg
```

```ts
backend.add(import('@backstage/plugin-search-backend'));
backend.add(import('@backstage/plugin-search-backend-module-pg'));
```

```yaml
search:
  pg:
    highlightOptions:
      useHighlight: true
      maxWord: 35
      minWord: 15
```

The highlight options default to enabled (`useHighlight: true`), `maxWord: 35` and `minWord: 15`; `highlightAll` defaults to false. Highlighting uses `ts_headline`, which can affect performance, so set `useHighlight: false` to disable it.

Elasticsearch and OpenSearch have their own backend module and connection configuration (Elastic Cloud ID, OpenSearch node, API key or username and password). Supported versions: Elasticsearch 8.19 or later, OpenSearch 1.x and 2.x.

## Checked

2026-11-03. Confirmed against the Backstage Search Engines page: three engines, Lunr default and discouraged in production, Postgres 12 requirement, highlight option defaults, supported Elasticsearch and OpenSearch versions. Removed: the no-migration claim and the one-module rule (not in the page).

Method: documentation only; no commands were run.
