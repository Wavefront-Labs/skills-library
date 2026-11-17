---
id: computing-software.data-engineering.dbt.overriding-package-sources
name: overriding-package-sources
category: computing-software
field: data-engineering
product: dbt
tags: [dbt, source-overrides, packages, sources, fivetran-packages]
level: advanced
status: docs-checked
description: "Point a dbt package's sources at your real database and schema with overrides, instead of forking the package, and how vars-based package configs differ."
sources:
  - https://docs.getdbt.com/reference/resource-properties/overrides
  - https://docs.getdbt.com/docs/build/packages
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Overriding package sources

**Goal:** use a source package (Fivetran/community packages) whose `sources:` assume a database/schema you do not have.

## overrides
In your project, declare a source with the **same name** as the package's source and `overrides: <package_name>`. The dbt docs mark the `overrides` property as deprecated in v1.10 and say to enable or disable a source from a package instead, so check the current page for your version.
```yaml
# models/staging/_package_overrides.yml
version: 2
sources:
  - name: stripe               # name of the source in the package
    overrides: stripe_source   # package (project) name
    database: raw
    schema: stripe_eu
    tables:
      - name: charge
        loaded_at_field: _loaded_at
```
The properties you set are applied on top of the package source's base properties. Overridable source properties per the docs: description, meta, database, schema, loader, quoting, freshness, loaded_at_field, tags.

## Many packages use vars instead
Check the package README: where a package offers vars for its source database and schema, those are the intended path.

## Gotchas
- The package name is the `name:` in the package's `dbt_project.yml`, not the hub repo name.
- Upgrading the package can rename sources, so overrides can stop matching; pin package versions.

## Verify
`dbt compile --select package:stripe_source` and check compiled `from` clauses point at `raw.stripe_eu...`.

## Checked

2026-10-28. Confirmed against: overrides property page (deprecation note, overridable property list, Fivetran example), packages page. Removed (not confirmable in the fetched pages): identifier override, no-new-tables claim, test/description retention claim, vars example keys.

Method: documentation only; no commands were run.
