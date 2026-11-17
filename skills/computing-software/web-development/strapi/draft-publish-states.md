---
id: computing-software.web-development.strapi.draft-publish-states
name: draft-publish-states
category: computing-software
field: web-development
product: strapi
tags: [strapi, draft-and-publish, status, modified, published, content-manager]
level: intro
status: docs-checked
description: "Draft and Publish in Strapi: the Published, Modified and Draft statuses, the Draft and Published tabs, and where API defaults differ."
sources:
  - https://raw.githubusercontent.com/strapi/documentation/main/docusaurus/docs/cms/features/draft-and-publish.md
  - https://raw.githubusercontent.com/strapi/documentation/main/docusaurus/docs/cms/api/rest/status.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Draft and Publish

An entry has one of three statuses:

- Published: previously published, no pending draft changes.
- Modified: previously published; draft changes saved but not yet published.
- Draft: never published.

## In the Content Manager
- Edit view tabs: **Draft** (editable) and **Published** (read-only view of the published content).
- In list view, filter entries by status with **Filters** and sort by clicking the **Status** column header.

## In code
Toggle in the schema `options` with `draftAndPublish`. API behavior:
- REST defaults to `published` on every request including `POST`/`PUT` (`status=draft` to stay draft).
- Document Service defaults to `draft`; `publish()`, `unpublish()`, `discardDraft()` exist only with this feature.
- `unique` attribute checks are skipped on draft saves (see `computing-software.web-development.strapi.database-column-settings`).

See `computing-software.web-development.strapi.rest-status-parameter` and `computing-software.web-development.strapi.document-service-publish`.

## Checked

2026-11-04: checked against the Strapi docs pages Draft & Publish (features/draft-and-publish) and REST API: status (api/rest/status). Confirmed: the three statuses, Draft and Published tabs, list filters and Status column sort, the `draftAndPublish` option, publish/unpublish/discardDraft only with the feature, REST default of published versus Document Service default of draft. Removed: nothing.

Method: documentation only; no commands were run.
