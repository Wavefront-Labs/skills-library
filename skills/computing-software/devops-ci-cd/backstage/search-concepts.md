---
id: computing-software.devops-ci-cd.backstage.search-concepts
name: search-concepts
category: computing-software
field: devops-ci-cd
product: backstage
tags: [search-concepts, collators, decorators, backstage]
level: intro
status: docs-checked
description: "Learn the Backstage Search building blocks: engines, collators, decorators, indices and the scheduler."
sources:
  - https://backstage.io/docs/features/search/concepts
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Backstage Search is an interface between your instance and a search engine of your choice. Its concepts are:

- Search engines: a `SearchEngine` is an interface with implementations for Lunr (in memory, the default), Postgres and Elasticsearch or OpenSearch.
- Query translators: convert an abstract query (terms, filters, document types) into the engine's query language.
- Documents: abstract searchable items whose metadata includes at least a title, text and location (a URL).
- Collators: produce the documents for an index by reading from a source, such as the catalog or TechDocs.
- Decorators: modify documents produced by collators before indexing, for example adding fields or removing sensitive ones.
- The scheduler: runs collation and decoration on a schedule.
- The search page, with a search context and reusable components for filters and results.

```ts
backend.add(import('@backstage/plugin-search-backend'));
backend.add(import('@backstage/plugin-search-backend-module-catalog'));
backend.add(import('@backstage/plugin-search-backend-module-techdocs'));
```

One collator defines and collects documents of one type. Backstage Search completely rebuilds indices on a schedule, and different collators can refresh at different intervals; when indexing is spread over several backend nodes a distributed `SchedulerServiceTaskRunner` coordinates them.

## Checked

2026-11-03. Confirmed against the Backstage Search Concepts page: the concept list, Lunr as the in-memory default, decorators between collator and indexer, rebuild-on-schedule behaviour. Removed: the per-type index claim, the design remark about non-catalog content and the troubleshooting advice (not in the page).

Method: documentation only; no commands were run.
