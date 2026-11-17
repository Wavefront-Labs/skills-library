---
id: computing-software.web-development.hasura.hasura-remote-schema-namespacing
name: hasura-remote-schema-namespacing
category: computing-software
field: web-development
product: hasura
tags: [hasura, remote-schemas, customization, namespace, type-names]
level: advanced
status: docs-checked
description: "Avoid remote schema type and field name conflicts in Hasura with root_fields_namespace, type_names prefix or suffix and field_names customization."
sources:
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/remote-schemas/namespacing-remote-schemas.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: merge schemas that define types with the same name.

Hasura checks for type conflicts automatically. If two schemas share a top-level type definition you may see an error starting `Found conflicting definitions for GraphQL type 'collections_order_by'` (the type name varies; the message goes on to list where the definitions differ). Hasura resolves this with namespaces or prefixes.

Where to set it: Remote Schemas tab, after filling in the schema's details click GraphQL Customizations; or the `customization` block in `remote_schemas.yaml`; or the `add_remote_schema` API.

The `customization` block holds:
- `root_fields_namespace`: namespace for the remote schema's root fields.
- `type_names`: `prefix`, `suffix` and a `mapping` of individual type names to new names.
- `field_names`: a list of entries with `parent_type`, `prefix` and a `mapping` of field names.

API template from the page:

```json
{ "type": "add_remote_schema",
  "args": { "name": "your remote schema name",
    "definition": {
      "url": "https://remote-server.com/graphql",
      "forward_client_headers": false,
      "timeout_seconds": 60,
      "customization": {
        "root_fields_namespace": "your_field_name",
        "type_names": { "prefix": "your_type_name_prefix",
                        "mapping": { "some_type_name": "some_new_type_name" } },
        "field_names": [ { "parent_type": "your_type_name",
                           "prefix": "your_field_name_prefix",
                           "mapping": { "some_field_name": "some_new_field_name" } } ] } } } }
```
Apply metadata with `hasura metadata apply`.

## Checked
2026-11-07. Read in full the single cited page (namespacing-remote-schemas.mdx; GitHub file view, no snippet files).
Confirmed: error text, customization keys, console label, API template.
Removed: the invented countries example and its claimed resulting query/type names, "customized names must be used in relationships and permissions" gotcha (not on the page), the invented Verify step. No `suffix` is listed under `field_names` because the page shows only `parent_type`, `prefix` and `mapping` there.
Method: documentation only; no commands were run.
