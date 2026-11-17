---
id: computing-software.software-engineering.api-design.graphql-federation
name: graphql-federation
category: computing-software
field: software-engineering
product: api-design
tags: [api-design, graphql, graphql-federation, apollo-federation, supergraph, subgraphs, entities, schema-composition, router, composite-schemas]
level: advanced
status: draft
description: "Split a GraphQL API across teams with federation: subgraphs and entities (@key), schema composition checks, the router, and when federation is overkill."
sources: ["https://www.apollographql.com/docs/graphos/schema-design/federated-schemas/federation", "https://www.apollographql.com/docs/graphos/schema-design/federated-schemas/entities/intro", "https://graphql.github.io/composite-schemas-spec/draft/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# GraphQL federation

**Goal:** one graph for clients, owned by many teams/services, without a monolithic
gateway schema that every team has to edit.

## Concepts
- **Subgraph**: a GraphQL service owning part of the schema.
- **Supergraph**: the composed schema; a **router** (Apollo Router, Cosmo, Hive
  Gateway, WunderGraph) plans queries across subgraphs.
- **Entity**: a type several subgraphs contribute fields to, identified by `@key`.

```graphql
# products subgraph
type Product @key(fields: "id") {
  id: ID!
  name: String!
  price: Money!
}

# reviews subgraph
type Product @key(fields: "id") {
  id: ID!
  reviews(first: Int = 10): [Review!]!      # adds a field to Product
}
```
The reviews subgraph implements a reference resolver (`__resolveReference({ id })`) so
the router can fetch `reviews` for products returned by the products subgraph.

## Composition and checks
- Compose in CI (`rover supergraph compose` / registry schema checks) on every subgraph
  change; composition errors (conflicting field types, missing keys, unresolvable
  fields) must fail before deploy.
- Operation checks against recorded client traffic catch breaking changes (removed
  fields still in use).
- Publish subgraph schemas to a registry; the router pulls the composed supergraph.

## Design rules
- Model the graph by domain, not by service boundaries leaking into types.
- Keys should be stable, cheap to resolve ids; avoid compound keys unless needed.
- Watch N+1 across subgraphs: reference resolvers receive batches; use DataLoader in
  each subgraph.
- Shared value types (`Money`) need `@shareable` and identical definitions.
- Auth: enforce at the router (JWT validation, `@authenticated`/`@requiresScopes`) AND in
  subgraphs; subgraphs must not be publicly reachable.

## When not to federate
A single team or a handful of services: a monolithic GraphQL server (or schema
stitching in the BFF) is simpler. Federation pays off when many teams need independent
deploys of graph changes.

## Standards
The GraphQL Foundation's Composite Schemas spec is standardising federation semantics
across vendors; Apollo Federation v2 is the de facto implementation today.

## Verify
- [ ] Schema/composition checks block a PR that removes a field used by clients.
- [ ] Query plans for hot queries inspected; no unexpected sequential fetch chains.
