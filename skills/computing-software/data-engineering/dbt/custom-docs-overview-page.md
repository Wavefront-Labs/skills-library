---
id: computing-software.data-engineering.dbt.custom-docs-overview-page
name: custom-docs-overview-page
category: computing-software
field: data-engineering
product: dbt
tags: [dbt, docs-overview-block, dbt-docs, doc-blocks, documentation]
level: intro
status: docs-checked
description: "Replace the default dbt docs landing page with a custom __overview__ doc block and per-package overviews, linking to models and onboarding guidance."
sources:
  - https://docs.getdbt.com/docs/build/documentation
  - https://docs.getdbt.com/reference/resource-properties/description
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom docs overview page

**Goal:** the first page of the docs site explains the project (layers, owners, how to find things) instead of dbt's generic text.

## Project overview
Create a docs block in a `.md` file in any resource path (dbt searches all resource paths by default, for example `models/overview.md`):
```markdown
{% docs __overview__ %}
# Analytics warehouse

- **staging**: one model per source table, renamed and typed.
- **marts/finance**: owned by #finance-data, refreshed hourly.
- Start with the models in `marts/`.

Questions: #data-help
{% enddocs %}
```
`dbt docs generate` picks it up; the name `__overview__` overrides the default overview.

## Per-package overview
```markdown
{% docs __dbt_utils__ %}
Utility macros. See the package README for usage.
{% enddocs %}
```
A docs block named `__<project_name>__` sets the overview shown when a viewer navigates inside that project or package.

## Tips
- Docs block names must be unique; `__overview__` and `__<project_name>__` are the special names.
- Keep it short; detailed docs belong on the models.

## Verify
`dbt docs generate && dbt docs serve`; the landing page shows your overview and links resolve.

## Checked

2026-10-25: dbt docs, current branch of dbt-labs/docs.getdbt.com (last commit 2026-10-23). Confirmed: dbt documentation page: `__overview__` docs block overrides the default overview, `__<project_name>__` blocks set per-project/package overviews, docs blocks live in `.md` files found in all resource paths, and `dbt docs generate` / `dbt docs serve`. Removed unconfirmed model-link URL fragments and the asset-paths tip.

Method: documentation only; no commands were run.
