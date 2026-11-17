---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.backends-for-frontends
name: backends-for-frontends
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, design-patterns-cloud, backends-for-frontends, bff, api-composition, mobile-backend, graphql, token-handler, frontend-team-ownership]
level: practitioner
status: docs-checked
description: "Give each client type its own backend that shapes and aggregates APIs: ownership, what belongs in a BFF, the browser token-handler role, avoiding duplication."
sources: ["https://learn.microsoft.com/azure/architecture/patterns/backends-for-frontends", "https://samnewman.io/patterns/architectural/bff/", "https://datatracker.ietf.org/doc/draft-ietf-oauth-browser-based-apps/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Backends for frontends

## When
A shared general-purpose backend serves several interfaces whose needs differ: mobile devices
want different, fewer calls and less data than desktop, and one deployable artifact becomes a
bottleneck for change. Create a BFF for each interface; the Microsoft pattern page also lists
frontend teams' control of language, release cadence and prioritisation as a benefit.
Skip it when a single client exists or when GraphQL with frontend-specific resolvers already
lets clients ask for the data they need (the Azure page says BFFs might add no value then).
Newman notes desktop web on strong connections can often call downstream services directly.

## Rules
1. **One BFF per user experience, maintained by the team that owns the UI** (Sam Newman:
   "one experience, one BFF"). If iOS and Android experiences are very similar, one BFF is easier to
   justify; if they diverge greatly, separate BFFs make more sense. Sharing a BFF across
   interfaces complicates its growth and support (Azure).
2. A BFF aggregates calls to downstream services and shapes responses for its UI; it can also
   serve third parties that need a specific API.
3. Duplication between BFFs is a likely outcome (Azure): weigh it against a better-tailored
   experience. Remedies per Newman: extract shared functionality into a new service modelled
   on the domain, or push aggregation downstream.
4. **Browser security**: for browser-based apps the BFF acts as the OAuth confidential client,
   manages access and refresh tokens in a cookie-based session so no tokens reach the browser, and
   forwards requests to the resource server with the access token added. The IETF OAuth
   browser-based apps document notes HttpOnly cookies stop an attacker reading session state, and
   says the BFF SHOULD set `SameSite=Strict` on its cookies.

## Gotchas
- The BFF adds a network hop, so review latency against the service-level objectives (Azure).
- Each BFF is another backend to build and run, with technical debt if the effort is underestimated.

## Verify
- [ ] Each BFF has a single owning team.
- [ ] No access tokens visible in browser storage (devtools check).
- [ ] Cookies carry HttpOnly and SameSite=Strict.

## Checked
2026-11-08. Confirmed against the Azure Architecture Center BFF pattern page, Sam Newman's BFF article and the IETF OAuth browser-based apps document (section 6.1 BFF; the URL now resolves to RFC 10017). Removed unsupported claims: SSR, sparse fieldsets, caching/protocol translation duties, null-plus-error-flag partial responses, mobile contract pinning, N x M dependency edges, fan-out timeouts and p99 load test advice.
Method: documentation only; no commands were run.
