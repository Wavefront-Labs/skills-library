---
id: computing-software.web-development.hasura.hasura-allow-list
name: hasura-allow-list
category: computing-software
field: web-development
product: hasura
tags: [hasura, security, allow-list, query-collections, production]
level: practitioner
status: docs-checked
description: "Restrict Hasura to an allow list of approved operations with HASURA_GRAPHQL_ENABLE_ALLOWLIST and query collections, optionally per role."
sources:
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/security/allow-list.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: only run pre-approved GraphQL operations in production.

Enable it with env var `HASURA_GRAPHQL_ENABLE_ALLOWLIST=true` or flag `--enable-allowlist` (default `false`). Validation is not enforced for the `admin` role.

Metadata: define a query collection in `metadata/databases/query_collections.yaml`, then apply with `hasura metadata apply`:

```yaml
- name: allowed-queries
  definition:
    queries:
      - name: getAuthors
        query: |
          query { authors { id name } }
```
and add it to `metadata/databases/allow_list.yaml`:

```yaml
- collection: allowed-queries
```
Console: the `API` tab, `Allow List` section; add an operation (each needs a unique name) or upload a file. Role-based allow lists are available on Cloud/Enterprise from v2.3 (Console from v2.13); in OSS role-based entries are ignored.

Gotchas from the docs:
- Queries are validated against the schema; an invalid query gives an inconsistent Metadata error.
- The order of fields is compared strictly, so a reordered query is rejected; `__typename` is ignored.
- Introspection queries your clients need must be added explicitly.
- You can edit the list without enabling it.

## Checked

2026-11-04. Confirmed against the cited pages: allow-list page: env var and flag, default false, admin exemption, file paths, Console location, role-based availability, strict field order. Removed or corrected: wrong Console path (Security tab), invented workflow and Verify step.

Method: documentation only; no commands were run.
