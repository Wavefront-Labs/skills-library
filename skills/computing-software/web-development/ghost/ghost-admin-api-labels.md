---
id: computing-software.web-development.ghost.ghost-admin-api-labels
name: ghost-admin-api-labels
category: computing-software
field: web-development
product: ghost
tags: [ghost, admin-api, labels, members, segments]
level: intro
status: docs-checked
description: "Manage Ghost member labels through the Admin API, including count.members include and create, update and delete calls."
sources:
  - https://github.com/TryGhost/docs/blob/main/admin-api/labels/overview.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: organise members into internal segments.

Labels let publishers organise members into internal segments. They can be applied when creating or updating members, and managed directly through the labels resource.

Label object keys: `id`, `name`, `slug` (generated from the name), `created_at`, `updated_at`, and `count` when requested.

Parameters on retrieval: `include`, `filter`, `fields`, `limit`, `page`, `order`. The documented include value is `count.members`, which returns how many members hold each label. Browse paging and ordering behave as in the Content API.

Operations:
- Create: `POST /admin/labels/` with `{"labels":[{"name":"VIP"}]}`.
- Update: `PUT /admin/labels/{id}/` with the new name.
- Delete: `DELETE /admin/labels/{id}/`.

Usage idea: label an import batch or a group of event attendees.

Verify: browse labels with `include=count.members` and confirm each label's count matches the members you applied it to.

## Checked

2026-11-04. Confirmed: label object keys, parameters, count.members include, create, update and delete calls (labels overview page). Removed: the claim that labels are plain strings so renames propagate, the label-hygiene advice and the filter-menu claim.

Method: documentation only; no commands were run.
