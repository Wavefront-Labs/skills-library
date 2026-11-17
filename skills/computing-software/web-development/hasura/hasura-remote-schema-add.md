---
id: computing-software.web-development.hasura.hasura-remote-schema-add
name: hasura-remote-schema-add
category: computing-software
field: web-development
product: hasura
tags: [hasura, remote-schemas, graphql-stitching, headers, timeout]
level: practitioner
status: docs-checked
description: "Merge an external GraphQL server into Hasura as a remote schema with URL, headers, header forwarding, timeout and customization."
sources:
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/remote-schemas/adding-schema.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: expose another GraphQL API through the Hasura endpoint.

Details to specify when merging:
- Remote Schema name: an alias, unique on an instance.
- GraphQL server URL: entered manually or taken from an environment variable.
- Headers: toggle forwarding all client headers; send additional static name-value pairs and/or header name to environment-variable pairs (for secrets such as `X-Api-Key`).
- Optionally a separate list of introspection headers. Enabled with an empty list, introspection sends no configured headers; disabled, introspection uses the additional headers. Runtime operations always use the additional headers.

Console: Remote Schemas tab -> Add. In metadata, `remote_schemas.yaml`:

```yaml
- name: my-remote-schema
  definition:
    url: https://<REMOTE_HOST>/graphql
    timeout_seconds: 60
    forward_client_headers: true
```
Apply with `hasura metadata apply`, or call the `add_remote_schema` Metadata API with `name` and `definition` (`url`, `forward_client_headers`, `timeout_seconds`). Then query the remote fields through `/v1/graphql`.

Notes:
- Environment variables used in the URL or headers must be present with valid values when the schema is added (start the engine with them). With Docker, the container must be able to reach the endpoint.
- Top-level field names must be unique across merged schemas (case-sensitive). Types with the same name and structure merge; the same name with a different structure causes type conflicts.
- The remote schema is cached and refreshed only on explicit reload: Remote Schemas -> [name] -> Details -> Reload, or the `reload_remote_schema` API.
- Subscriptions on remote GraphQL servers are not supported.

## Checked
2026-11-07. Read in full the single cited page (adding-schema.mdx; GitHub file view, no snippet files).
Confirmed: every item above.
Removed: the header precedence claim, the Set-Cookie over WebSocket note, the "Found conflicting definitions for GraphQL type" error string, the `value_from_env` yaml key and `customization` mention (not on this page), "introspects when you add it" (the page says only cached and reloaded on request), and the invented Verify step. Added introspection headers and the reload steps.
Method: documentation only; no commands were run.
