---
id: computing-software.data-engineering.dbt.splitting-a-monolith-into-mesh-projects
name: splitting-a-monolith-into-mesh-projects
category: computing-software
field: data-engineering
product: dbt
tags: [dbt, mesh-project-split, dbt-mesh, cross-project-ref, multi-project]
level: sme
status: docs-checked
description: "Split a large dbt project into multiple dbt Mesh projects: choosing boundaries, public models with contracts, dependencies.yml, cross-project refs and the cutover."
sources:
  - https://docs.getdbt.com/best-practices/how-we-mesh/mesh-1-intro
  - https://docs.getdbt.com/docs/mesh/govern/project-dependencies
  - https://docs.getdbt.com/docs/mesh/govern/model-access
  - https://docs.getdbt.com/reference/commands/list
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Splitting a monolith into multiple projects

**Goal:** separate teams' code and deploys while keeping one consistent lineage, without breaking consumers.

## Choose boundaries
- Split by **team ownership / domain** (finance, marketing, platform core), not by layer.
- A good seam has few edges crossing it: list cross-team refs with `dbt ls --select +marts.finance --resource-type model` and look at what finance takes from others.
- First prepare inside the monolith: define `groups` with owners, set `access: private|protected|public`, and add `contract: {enforced: true}` to models that will cross the boundary. Fix violations there.

```yaml
groups:
  - name: finance
    owner: {name: Finance Data, email: finance-data@example.com}
models:
  - name: dim_customers
    group: finance
    access: public
    config: {contract: {enforced: true}}
```

## Create the downstream project
```yaml
# finance_project/dependencies.yml
projects:
  - name: core_platform
```
```sql
select * from {{ ref('core_platform', 'dim_customers') }}
```
Cross-project refs are resolved by a dbt metadata service from the upstream environment's public model metadata. The docs list this feature as available on dbt Enterprise or Enterprise+ plans; check the current docs for your plan. The upstream models must have `access: public` and at least one successful job run after `access` is defined.

## Cutover
1. Move finance models and their YAML to the new repo/project; keep relation names (schema/alias) identical so BI is unaffected.
2. Delete them from the monolith in the same release.
3. Add `deprecation_date` and model versions for any public model you plan to change.

## Gotchas
- Only `public` models can be referenced across projects; the docs say `protected` is limited to the same project (or installed as a package).
- dbt checks for node-level cycles across projects and raises errors if a new dependency introduces one.
- A project dependency does not pull source code; installing a project as a package does (and lets you call its macros). Use a package for shared macros.

## Verify
`dbt ls` in the downstream project resolves the upstream refs; prod relation names are unchanged before/after.

## Checked
2026-11-01. Confirmed against the dbt docs repo: `dependencies.yml` with upstream project names, cross-project `ref`, public-only cross-project access, protected scope, cycle checks, `deprecation_date` in model versions, `dbt ls --resource-type`. Removed: the dbt-loom plugin claim and the "deploy upstream first" ordering, neither stated in the docs.
Method: documentation only; no commands were run.
