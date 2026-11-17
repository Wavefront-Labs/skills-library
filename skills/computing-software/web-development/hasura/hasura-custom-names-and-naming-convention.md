---
id: computing-software.web-development.hasura.hasura-custom-names-and-naming-convention
name: hasura-custom-names-and-naming-convention
category: computing-software
field: web-development
product: hasura
tags: [hasura, naming-convention, custom-names, graphql-default, postgres, schema]
level: advanced
status: docs-checked
description: "Rename auto-generated Hasura fields with column_config custom_name and switch to the graphql-default (camelCase) naming convention on Postgres."
sources:
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/schema/postgres/custom-field-names.mdx
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/schema/postgres/naming-convention.mdx
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/deployment/graphql-engine-flags/reference.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: control the names Hasura generates.

Per-column rename in tables.yaml:

```yaml
- table:
    schema: public
    name: author
  configuration:
    column_config:
      addr:
        custom_name: address
```
Apply with `hasura metadata apply`. The same `column_config` can be passed to `pg_track_table`. Console: `Data -> [table-name] -> Modify`, click Edit on the field (custom root field names are under Custom GraphQL Root Fields).

Naming conventions (Postgres sources only):
- `hasura-default`: the default; snake_case, enum table values unchanged.
- `graphql-default`: types pascal-cased (table `my_table` in schema `my_schema` yields `MySchemaMyTable`), fields and arguments camel-cased (for example `mySchemaMyTableAggregate`), and enum values upper-cased.

The server-wide default is set with env var `HASURA_GRAPHQL_DEFAULT_NAMING_CONVENTION` (default `hasura-default`). Naming conventions are generally available from v2.34.0; before that, from v2.8.0, they were experimental and needed `naming_convention` in `HASURA_GRAPHQL_EXPERIMENTAL_FEATURES`.

Gotcha: custom table and field names set in Hasura override the naming convention.

## Checked

2026-11-04. Confirmed against the cited pages: custom-field-names and naming-convention pages plus flags reference: column_config custom_name, pg_track_table, Console path, the two conventions, Postgres-only, env var, v2.34.0 GA and v2.8.0 experimental flag. Removed or corrected: the claim that changing the convention breaks client queries (the page does not say) and the Verify step.

Method: documentation only; no commands were run.
