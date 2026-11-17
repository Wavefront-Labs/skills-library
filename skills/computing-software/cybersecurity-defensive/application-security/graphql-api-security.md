---
id: computing-software.cybersecurity-defensive.application-security.graphql-api-security
name: graphql-api-security
category: computing-software
field: cybersecurity-defensive
product: application-security
tags: [api-security, graphql-security, query-depth-limiting, query-cost-analysis, introspection, field-level-authorization, batching-attacks]
level: advanced
status: docs-checked
description: "Secure GraphQL APIs per the OWASP cheat sheet and graphql.org: business-layer authorization, depth, amount and cost limits, alias and batching abuse, introspection, errors."
sources: ["https://cheatsheetseries.owasp.org/cheatsheets/GraphQL_Cheat_Sheet.html", "https://graphql.org/learn/authorization/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GraphQL API security

One endpoint with a client-chosen query shape: authorization and resource limits must apply where data is resolved, not at the URL.

## Authorization
- graphql.org: put authorization in the business logic layer as a single source of truth, and have field resolvers delegate to it. Duplicating rules per entry point lets users see different data depending on which API they use. Authenticate first, then pass a hydrated user object into the business layer. Resolver-level checks are for learning or prototypes; an `@auth` directive can apply rules to fields but should still delegate.
- OWASP: check access to every object whether or not the caller knows its ID (IDOR, BOLA, BFLA); check both edges and nodes; authorise `node`/`nodes` fields (remove them if unneeded); apply field-level and mutation-level controls; use interfaces/unions or RBAC middleware to vary fields by role.

## Denial of service
- **Depth limit**: `graphql-depth-limit` (JS), `MaxQueryDepthInstrumentation` (graphql-java).
- **Amount limit**: cap list sizes (the example is `first: 99999999`) and paginate.
- **Timeouts** at application level (examples use 10 s); infrastructure timeouts are less accurate and easier to bypass.
- **Query cost analysis**: assign field costs and reject expensive queries (`graphql-cost-analysis`, `graphql-validation-complexity`, `MaxQueryComplexityInstrumentation`); Apollo advises confirming the need first.
- **Rate limiting** at HTTP level (nginx `limit_req`; Apache `mod_ratelimit` limits only bandwidth) plus GraphQL-aware limits in business logic. Use DataLoader to avoid duplicate fetches; limit resources with cgroups or Docker.

## Batching and aliases
Batching and aliases (`second:droid(id: "2001")`) pack many operations into one request, enabling brute force and enumeration that evades WAF, SIEM and HTTP-level limits. Count object requests in code, disable batching for logins, OTPs and tokens, and limit operations per request (helpful, not complete).

## Attack surface
- Disable introspection in production or public environments (`NoIntrospection` rule in JS; `NO_INTROSPECTION_FIELD_VISIBILITY` in Java); filter by consumer if some roles need it. Disable GraphiQL outside development. Disable field suggestions; brute force can still reveal fields.
- No stack traces in production (Apollo: `includeStacktraceInErrorResponses: false`); log details internally.
- Injection still applies: validate input with allowlists and specific types (scalars, enums, input types) and use parameterised APIs.

## Verify
Production rejects an introspection query and an over-deep query; an alias batch of logins is limited; a lower-privileged user cannot read a restricted field via any nesting path.

## Checked
Method: 2026-11-08 read the OWASP GraphQL Cheat Sheet (via summary of the full page) and graphql.org authorization page. The Apollo routing-security URL returns 404 and was removed from sources. Dropped as unsupported by these pages: the 7-10 depth figure, persisted queries / operation allowlists as a control, CSRF content-type advice, circular-fragment note and the named testing tools (InQL, graphql-cop, Clairvoyance). Other claims restated from the pages.
