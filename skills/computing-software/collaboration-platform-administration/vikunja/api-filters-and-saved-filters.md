---
id: computing-software.collaboration-platform-administration.vikunja.api-filters-and-saved-filters
name: api-filters-and-saved-filters
category: computing-software
field: collaboration-platform-administration
product: vikunja
tags: [vikunja, filter-query-api, filter-date-math, saved-filters-api, filter-field-names]
level: practitioner
status: docs-checked
description: "Query Vikunja tasks through the API with filter syntax: parameters, snake_case fields, IDs for labels and projects, date math and the saved filters endpoints."
sources:
  - https://raw.githubusercontent.com/go-vikunja/website/main/src/content/docs/integrations/filters.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Pass filters as query parameters when listing tasks, for example `GET /api/v1/projects/1/views/5/tasks?filter=due_date < now && done = false&sort_by=priority&order_by=desc` (URL-encoded).

Parameters: `filter`; `filter_include_nulls` (default false); `filter_timezone` (server timezone if unset); `s` (plain text search, cannot combine with `filter`); `sort_by` and `order_by` (comma-separated, asc/desc); `per_page`. Sortable: id, title, done, done_at, due_date, start_date, end_date, priority, percent_done, created, updated, position.

API fields are snake_case: `due_date`, `start_date`, `end_date`, `done_at`, `percent_done`, `created_by`. `created_by` matches usernames; use `created_by_id` for numeric ids. Labels and projects must be numeric IDs here (`labels in 1, 5`, `project = 12`); look them up with `GET /api/v1/labels` and `/projects`.

Date math: anchor `now` or `YYYY-MM-DD||`, then arithmetic and rounding: `now+7d`, `now/d`, `now-1M/M`, `2024-03-11||+1w`. Units s, m, h, d, w, M, y.

Saved filters: `GET|PUT /api/v1/filters`, `GET|POST|DELETE /api/v1/filters/{id}`. They show up in task listings as pseudo-projects with negative IDs (project -1 is filter 1).

## Checked

2026-11-04. Confirmed against the Vikunja Filter API Reference (integrations/filters): query parameters and sortable fields, snake_case field names, created_by vs created_by_id, numeric label and project IDs, date math anchors and units, saved filter endpoints and negative pseudo-project IDs. Nothing removed.

Method: documentation only; no commands were run.
