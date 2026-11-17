---
id: computing-software.data-engineering.dbt.project-dependencies-yml
name: project-dependencies-yml
category: computing-software
field: data-engineering
product: dbt
tags: [dbt, dbt-mesh, dependencies-yml, cross-project-ref, packages-yml, upstream-project, public-models]
level: advanced
status: docs-checked
description: "Wire dbt Mesh projects with dependencies.yml: declare upstream projects vs packages, two-argument ref, public models only, and how resolution works in dbt Cloud vs Core."
sources:
  - https://docs.getdbt.com/docs/collaborate/govern/project-dependencies
  - https://docs.getdbt.com/reference/dbt-jinja-functions/ref#ref-project-specific-models
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Project dependencies with dependencies.yml

**Goal:** a downstream dbt project references another team's public models without installing their code as a package.

## dependencies.yml
```yaml
# downstream project root
projects:
  - name: core_platform          # the upstream project's name in its dbt_project.yml
packages:                        # packages may live here too (or stay in packages.yml, not both)
  - package: dbt-labs/dbt_utils
    version: <VERSION>
```

## Referencing
```sql
select * from {{ ref('core_platform', 'dim_customers') }}
```
Only models with `access: public` in the upstream project can be referenced; see the ref page for pinning a model version.

## How it resolves
- **dbt Cloud (Enterprise):** the upstream project's production environment publishes metadata; the downstream resolves `ref` to the relation of the upstream's latest successful prod run. No upstream code is pulled.
- **Without that platform support:** use the upstream as a package (code dependency) instead; check the project-dependencies page for what is supported outside dbt Enterprise.

## Package vs project dependency
| | Package (`packages.yml`) | Project (`dependencies.yml` projects) |
|---|---|---|
| What is installed | upstream code; you can build its models | nothing; only metadata |
| Who builds upstream models | you could (risk of duplicate builds) | upstream team only |
| Access enforcement | none | only public models |
| Versioning | git tag/semver | model versions + contracts |

## Upstream obligations
- Mark interface models `access: public`, and use model contracts and versions for breaking changes (see the dbt model-governance docs).
- Keep prod runs healthy: downstream resolution follows the last successful prod deploy.

## Gotchas
- Downstream CI needs upstream metadata to resolve refs (dbt Cloud handles this; Core setups need the manifest available in CI).
- Renaming the upstream project breaks every two-argument ref.

## Verify
- [ ] The two-argument ref resolves in the downstream project.
- [ ] Referencing a non-public upstream model fails.

## Checked

2026-10-28. Confirmed against: project-dependencies page (dependencies.yml for projects, packages vs projects, Enterprise availability, upstream models with access: public and a successful production run), packages page (dependencies.yml alongside packages.yml). Removed (not confirmable in the fetched pages): dbt-loom, model version pin syntax, deprecation_date, contract syntax, circular-dependency claim, dbt ls external nodes, package version pin.

Method: documentation only; no commands were run.
