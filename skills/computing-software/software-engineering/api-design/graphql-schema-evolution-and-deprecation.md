---
id: computing-software.software-engineering.api-design.graphql-schema-evolution-and-deprecation
name: graphql-schema-evolution-and-deprecation
category: computing-software
field: software-engineering
product: api-design
tags: [api-design, graphql, graphql-schema-evolution, deprecated-directive, schema-registry, breaking-changes]
level: practitioner
status: docs-checked
description: "Evolve a versionless GraphQL schema: additive change, @deprecated with reasons, usage-aware breaking-change checks in CI and removal only when unused."
sources: ["https://graphql.org/learn/best-practices/", "https://spec.graphql.org/draft/#sec--deprecated", "https://the-guild.dev/graphql/inspector/docs/commands/diff", "https://www.apollographql.com/docs/graphos/platform/schema-management/checks"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GraphQL schema evolution and deprecation

GraphQL's own best-practices guide describes designing and evolving a type system over time
**without versions**: prefer adding to the schema and retire old parts deliberately.

## Deprecate, track, remove
```graphql
type User {
  name: String @deprecated(reason: "Use `displayName`. Removal after 2027-03-01.")
  displayName: String!
}
```
The `@deprecated` directive takes a `reason` (default "No longer supported", formatted as
CommonMark Markdown). In the current draft spec it is allowed on field definitions, argument
definitions, input field definitions, enum values and directive definitions; the October 2021
edition covers fields and enum values only, so check your server library before deprecating
arguments or input fields. It must not be put on a required argument or input field (non-null
without a default): make it optional first.
Introspection's `fields`, `enumValues` and `directives` take `includeDeprecated` (default false).

Remove only when usage is zero. Use operation-usage data from your registry or your own
resolver metrics, per client.

## CI checks
Compare the proposed schema with the current one and fail the build on breaking changes:
```
graphql-inspector diff OLD_SCHEMA NEW_SCHEMA
```
GraphQL Inspector treats removal of a deprecated field as breaking by default; its
`suppressRemovalOfDeprecatedField` rule downgrades that, and `considerUsage` with `--onUsage`
decides whether a breaking change really is one from real usage data. Apollo GraphOS schema
checks do the same from historical client operations (build and operations checks run by default).

## Patterns
- Replace a field's type by adding a new field (`priceV2: Money!`), deprecating the old one.
- Expand-then-contract for arguments: add optional, migrate clients, then change.

## Checked
2026-11-01. Confirmed: the draft spec's @deprecated definition, locations, reason default, Markdown
reason and required-argument restriction; the October 2021 spec's narrower wording (fields, enum
values); includeDeprecated defaults in the draft introspection schema; the graphql.org best-practices
"evolve without versions" lesson summary; GraphQL Inspector diff usage and the two rules named;
Apollo checks (build and operations by default). Removed: safe-vs-breaking table, rover command,
git: schema-source syntax, persisted-query, header, GraphQL Hive and federation statements, IDE
strikethrough claim (not stated in the cited pages).
Method: documentation only; no commands were run.
