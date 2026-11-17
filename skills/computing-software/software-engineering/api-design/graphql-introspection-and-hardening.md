---
id: computing-software.software-engineering.api-design.graphql-introspection-and-hardening
name: graphql-introspection-and-hardening
category: computing-software
field: software-engineering
product: api-design
tags: [api-design, graphql, graphql-introspection, graphql-security, query-depth, batching-attacks, field-suggestions, api-security]
level: advanced
status: docs-checked
description: "Understand GraphQL introspection and harden endpoints: decide whether to disable it, remove suggestions, bound depth and batching, auth per field."
sources: ["https://spec.graphql.org/October2021/#sec-Introspection", "https://graphql.org/learn/introspection/", "https://cheatsheetseries.owasp.org/cheatsheets/GraphQL_Cheat_Sheet.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GraphQL introspection and hardening

## What introspection is
The `__schema` field is available on the query root operation type (and `__type` for single types); tools like GraphiQL, codegen and schema registries depend on them.
```graphql
{ __schema { queryType { name } types { name kind } } }
```

## Decide, then enforce
- Public APIs for third parties usually keep introspection on (it is the documentation). Internal or first-party-only APIs commonly disable it in production; this is obscurity, not authorization, and attackers can still guess names.
- graphql.org notes introspection is often disabled in production, and is typically unneeded for APIs used only by your own apps whose operations are baked in at build time. OWASP says to disable it system-wide in production or publicly accessible environments, or to allow it only for approved consumers or roles. How to disable it is server-specific; check your server's docs.
- Disable field-name suggestions ("Did you mean ...?") in production responses; the OWASP cheat sheet lists suggestion of mis-typed fields as a leak when introspection is disabled.

## Other limits to set
- Maximum query depth and complexity/cost; see the query-complexity guidance in graphql-schema-design.
- Limit batching: OWASP describes batching attacks (many object instances or operations in one call, a brute-force form) and mitigates them with a code-level limit on objects requested, no batching for sensitive objects (usernames, emails, OTPs, session tokens) and a cap on batched operations. graphql.org lists alias limits among depth, breadth and cost controls. Apply rate limits in the business-logic layer together with cost and batching limits, since HTTP request counts miss multi-operation requests.
- Use operation safe-listing (persisted queries) for first-party clients where possible.
- Enforce authorization in resolvers or the data layer, per field.
- Disable debug mode and stack traces; do not return excessive error messages.

## Gotchas
- Turning off introspection breaks client codegen in CI unless it uses a checked-in schema file or a registry (inference, not stated in the sources).

Verify: send the `__schema` query to production; the response should match your policy. Send a typo'd field and confirm no suggestion text. Send a query with many aliases or batched operations and confirm it is rejected.

## Checked
2026-11-08. Confirmed in the OWASP GraphQL Cheat Sheet (read by targeted search: introspection, GraphiQL, suggestions, depth limiting, batching mitigations, error and stack-trace guidance) and the graphql.org introspection page (`__schema`, "Introspection in production"). The GraphQL spec page cited was fetched but is the whole specification and was only searched, not read in full. Removed: the Apollo Server 4 `NODE_ENV` default and `introspection: true` claim, the GET/CSRF mutation advice and the 50-alias figure, none supported by the cited pages.
Method: documentation only; no commands were run.
