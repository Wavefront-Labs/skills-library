---
id: computing-software.data-engineering.dbt.model-contracts-and-governance
name: model-contracts-and-governance
category: computing-software
field: data-engineering
product: dbt
tags: [dbt, dbt-contracts, model-versions, access-modifiers, dbt-groups, dbt-mesh, dbt-governance, public-models, protected-models, breaking-changes, semantic-layer, cross-project-ref, model-constraints]
level: advanced
status: verified
description: "Use dbt model contracts, versions, access modifiers and groups to govern a multi-team project without breaking downstream consumers."   # quoted: YAML would cut an unquoted value at " #" or choke on ": "
sources:
  - https://docs.getdbt.com/docs/collaborate/govern/model-contracts
  - https://docs.getdbt.com/docs/collaborate/govern/model-access
  - https://docs.getdbt.com/docs/collaborate/govern/model-versions
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# dbt governance — contracts, access, versions and groups

**Goal:** let multiple teams build on each other's dbt models without every change being a potential silent breaking change to someone else's pipeline.

## 1. Model contracts — enforce the shape, not just test the content
```yaml
models:
  - name: fct_orders
    config:
      contract: {enforced: true}
    columns:
      - name: order_id
        data_type: int
        constraints: [{type: not_null}, {type: primary_key}]
      - name: amount
        data_type: decimal(18,2)
```
With `contract: {enforced: true}`, dbt generates the `CREATE TABLE` DDL with the declared column names/types/constraints (for a table the debug SQL showed `order_id int not null primary key`, and a NULL violated it at build; a view got the column and type check) and fails the build if the SQL's actual output doesn't match — a changed column type, a renamed column, or a dropped column fails at build time with a clear contract-violation error, instead of silently changing the table shape and breaking a downstream consumer's query weeks later with no signal at the point of change. This is fundamentally different from `data_tests` (which check row-level content after the fact) — a contract checks structural shape before the data is even materialized.
- **Gotcha:** contracts require an explicit `data_type` on every column referenced, and some database-specific type aliasing (e.g. `string` vs `varchar`) must match exactly what the warehouse adapter expects — a contract failure that looks like a data-type mismatch is often just a type-name spelling difference between what you wrote and what the adapter normalizes to; check the adapter's exact type-name conventions. On dbt-duckdb a `string` contract type matched a `varchar` column, and a type mismatch printed a table such as `amount | DOUBLE | DECIMAL(18,2) | data type mismatch` (a renamed column showed `missing in definition` / `missing in contract`).

## 2. Access modifiers — control who can `ref()` what
```yaml
models:
  - name: fct_orders
    access: public      # private (default: protected) | protected | public
```
`private`: only referenceable within the same dbt **group**. `protected` (the implicit default): referenceable anywhere within the same dbt project. `public`: referenceable from other dbt projects (cross-project `ref()`, dbt Mesh). This turns "which models are safe for another team to build on" from a tribal-knowledge/naming-convention question (prefixing "internal" models with `_` and hoping nobody refs them) into an enforced one — a `ref()` to a `private` model from outside its group fails at parse time with a clear error (checked: "attempted to reference node ... which is not allowed because the referenced node is private to the 'finance' group").

## 3. Groups — the boundary a private model's privacy is scoped to
```yaml
groups:
  - name: finance
    owner: {name: "Finance team"}
```
A group is dbt's unit of ownership — models assigned to a group (`config: {group: finance}`) are private to that group; it's the organizational primitive contracts and access modifiers hang off of. A `private` model with no group is not shared with anything: a `ref()` to it failed at parse ("private to the '' group", checked), so assign a group before using `private`. An invalid access value (e.g. `internal`) is a parse error.

## 4. Model versions — evolve a public contract without breaking consumers mid-flight
```yaml
models:
  - name: dim_customer
    versions:
      - v: 1
        defined_in: dim_customer_v1
      - v: 2
        defined_in: dim_customer_v2
    latest_version: 2
```
Lets `ref('dim_customer', version=1)` and `ref('dim_customer', version=2)` coexist (both parsed; a plain `ref('dim_customer')` also parsed) — downstream consumers pin to the version they've tested against and migrate on their own schedule, rather than a breaking change to a public/protected model forcing every downstream team to update simultaneously the moment it merges. This is the mechanism that makes contracts + public access viable for genuinely multi-team dbt projects (or dbt Mesh across separate projects) instead of contracts just becoming a build-blocker every time a shared model needs to evolve.

## 5. Where this matters vs where it's overhead
Contracts, access modifiers, groups and versions earn their setup cost in multi-team dbt projects (or dbt Mesh's cross-project model) where a breaking change to a shared model is a cross-team incident. For a single small team's project, this is governance overhead without a corresponding problem — standard dbt data tests and code review are enough; don't bolt on contracts/groups/versions as a default best practice regardless of team size.

## Verify
- [ ] Every model with `access: public` has `contract: {enforced: true}` — public without a contract is an unenforced promise.
- [ ] A deliberate breaking change (renamed column) to a contracted model fails the build immediately, confirmed by testing it in a non-prod branch.
- [ ] Groups exist and map to actual team/ownership boundaries before `private` access is used anywhere.
- [ ] A versioned model's `latest_version` and each downstream `ref()`'s pinned version are both documented, so a version bump's blast radius is known before it ships.
