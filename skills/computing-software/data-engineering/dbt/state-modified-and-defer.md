---
id: computing-software.data-engineering.dbt.state-modified-and-defer
name: state-modified-and-defer
category: computing-software
field: data-engineering
product: dbt
tags: [dbt, dbt-core, slim-ci, state-modified, dbt-defer, state-flag, manifest-json, favor-state, production-artifacts, modified-subselectors]
level: advanced
status: gated
description: "Build only what changed with dbt state selection: state:modified+ against prod manifest, --defer to read unbuilt parents from prod, --favor-state, and modified sub-selectors."
sources:
  - https://docs.getdbt.com/reference/node-selection/state-selection
  - https://docs.getdbt.com/reference/node-selection/defer
  - https://docs.getdbt.com/reference/node-selection/methods#state
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# state:modified and --defer (Slim CI)

**Goal:** CI (or a dev session) builds and tests only changed models and their dependents, reading everything else from production.

## Ingredients
1. A **production manifest**: `target/manifest.json` from the latest successful prod run, stored somewhere CI can fetch (S3/GCS bucket, CI artifact, dbt Cloud does this automatically).
2. `--state <dir>` pointing at it.

## Command
```bash
aws s3 cp s3://<BUCKET>/dbt/prod-artifacts/manifest.json prod-state/manifest.json   # not run: no AWS account
dbt build --select state:modified+ --defer --state prod-state --target ci
```
- `state:modified` compares the current project to the prod manifest: changed SQL (body), configs (checked: a `materialized` change in YAML and in `config()`), upstream macros (checked), contracts, relation names, access/group/version fields, and seed contents (seeds under 1 MiB; at 1 MiB or more only a path change counts). `tags` and `meta` changes do not count (docs; a tags-only edit and a description-only edit selected nothing here), and a `description` change counts only with `persist_docs` on.
- `+` includes downstream dependents (they may break).
- `--defer`: when a selected model `ref`s a model **not** built in this run, resolve it to the **prod** relation instead of the empty CI schema. Without defer, CI would need to build all parents.
- `--favor-state` (introduced in 1.5 (gated: unconfirmed, source is paywalled or blocked)): prefer the prod relation even if a dev/CI relation exists. Deferral was checked: with `--defer --state prod-state --target ci`, `fct_orders` built in the CI schema while its parents resolved to `main.stg_orders`; without `--defer` the build failed because the parents were missing.

## Sub-selectors
`state:modified.body`, `.configs` (excludes database, schema, alias, tags, meta), `.relation`, `.persisted_descriptions`, `.macros`, `.contract`; `state:new` for brand-new nodes. Useful to skip rebuilds for doc-only changes: `-s state:modified.body+ state:modified.configs+`.

## Gotchas
- Macro changes mark every model using the macro as modified (can be large).
- Env-dependent Jinja (`target.name` branches, `env_var`) or differing vars in config can make models look modified if CI renders differently from prod (untested here (gated: unconfirmed, source is paywalled or blocked)); keep rendered SQL environment-stable.
- The prod manifest should come from a compatible dbt version (manifest schema versions differ between releases; exact compatibility rule (gated: unconfirmed, source is paywalled or blocked)).
- Deferred parents are prod data: tests in CI read prod (permissions!) and CI results reflect prod state.

## Verify
- [ ] A PR touching one model builds that model + children only (`dbt ls -s state:modified+ --state prod-state` matches expectation).
- [ ] CI role has read access to prod schemas used via defer and write only to CI schemas.
