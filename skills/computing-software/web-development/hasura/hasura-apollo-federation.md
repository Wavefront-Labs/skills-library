---
id: computing-software.web-development.hasura.hasura-apollo-federation
name: hasura-apollo-federation
category: computing-software
field: web-development
product: hasura
tags: [hasura, federation, apollo, subgraph, schema-registry]
level: sme
status: docs-checked
description: "Run Hasura as an Apollo Federation v1 subgraph with HASURA_GRAPHQL_ENABLE_APOLLO_FEDERATION and know the Cloud Schema Registry."
sources:
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/data-federation/overview.mdx
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/data-federation/apollo-federation.mdx
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/data-federation/schema-registry.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: include Hasura in a federated supergraph.

Availability: Apollo Federation v1 spec, from v2.10.0. Enable on the server with the flag `--enable-apollo-federation` or:

```bash
HASURA_GRAPHQL_ENABLE_APOLLO_FEDERATION=true
```
Then enable each table explicitly (Console: `Data -> [table-name] -> Modify`, Enable Apollo Federation) or in the table's metadata YAML:

```yaml
apollo_federation_config:
  enable: v1
```
Behaviour per the docs: only types generated for database source tables can be extended in other subgraphs; the primary key is used in the `@key` directive, for example `type user @key(fields: "id")`. Hasura types can be used to extend other subgraphs, but extending Hasura types from other subgraphs is not possible; the docs recommend remote relationships for that. Action types and Remote Schema types cannot be extended.

Schema Registry (Hasura Cloud, v2.26.0-cloud.1 and later): stores the GraphQL schemas (for all defined roles) whenever an operation could change them: applying metadata, reloading metadata or a Hasura version update. It is found under the `API` tab.

Gotcha: if you enable federation from the Console, `apollo_federation` must first be added to `HASURA_GRAPHQL_EXPERIMENTAL_FEATURES` (or `--experimental-feature`).

## Checked

2026-11-04. Confirmed against the cited pages: apollo-federation and schema-registry pages: v1 spec, v2.10.0, flag and env var, per-table apollo_federation_config, @key from primary key, extension direction, unsupported types, experimental-features prerequisite for the Console, Schema Registry triggers and v2.26.0-cloud.1. Removed or corrected: gateway registration step, the data-federation comparison, the self-correction gotcha and the Verify step.

Method: documentation only; no commands were run.
