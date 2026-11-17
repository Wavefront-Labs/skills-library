---
id: computing-software.software-engineering.software-architecture.api-gateway-and-backend-for-frontend
name: api-gateway-and-backend-for-frontend
category: computing-software
field: software-engineering
product: software-architecture
tags: [software-architecture, api-gateway, backend-for-frontend, bff, edge-services, gateway-aggregation]
level: practitioner
status: docs-checked
description: "Use an API gateway for cross-cutting edge concerns and backend-for-frontend services per client type, without turning either into a business-logic monolith."
sources: ["https://microservices.io/patterns/apigateway.html", "https://samnewman.io/patterns/architectural/bff/", "https://learn.microsoft.com/en-us/azure/architecture/microservices/design/gateway"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# API gateway and backend-for-frontend

## API gateway
A single entry point for all clients, acting as a reverse proxy. Some requests are routed to the right service; others fan out to several services and are composed (the API composition pattern).
- Why: microservice APIs are fine-grained, different clients need different data, mobile networks are slower than a LAN so a mobile client can make only a few calls, and service locations and partitioning change and should be hidden from clients.
- Cross-cutting work it can offload (Microsoft's list): SSL termination, mutual TLS, authentication, client rate limiting (throttling), logging and monitoring, response caching. It also provides layer-7 routing.
- Benefits: insulates clients from service partitioning and instance locations, gives each client an optimal API, cuts round trips, simplifies clients, and can translate a public web-friendly protocol to internal ones.
- Drawbacks: one more moving part to develop, deploy and manage, and an extra network hop (Richardson: for most applications the cost is insignificant).
- Choose a gateway that supports every feature you need: all common options support layer-7 routing, but support for authentication, rate limiting and SSL termination varies. A mesh ingress gateway typically has weaker WAF, API productisation, request transformation and global routing than a dedicated API gateway.
- When services or routes change, update routing rules, certificates, IP allow lists and security configuration through infrastructure as code and automation.
- It may authenticate the user and pass an access token with user information to services, and it should call services through a circuit breaker.

## Backend-for-frontend (Sam Newman)
A separate gateway/backend per kind of client (for example web app, mobile app, external third-party app), tightly coupled to one user experience and typically maintained by the team that builds that user interface.
- Problem it solves: one general-purpose API backend must serve several user-facing applications, so it becomes a bottleneck for delivery (many changes to the same deployable), and mobile needs different, fewer calls and less data than desktop.
- Reuse pressure leads some teams to fewer BFFs; duplication across BFFs can be handled by pushing aggregation further downstream or by a shared library (with the usual shared-library caveats in microservices).
- Without BFFs, common logic tends to get baked into the clients, on very different tech stacks, which makes duplication hard to spot; duplication across BFFs on a common server stack is easier to spot and factor out.
- Desktop web is often delivered on better devices and connectivity, where multiple downstream calls are manageable, so it may not need a BFF.
- Example setups from the page: a different BFF per mobile platform (REA) and one BFF for different mobile backends (SoundCloud).

## Layout
Client -> gateway (cross-cutting concerns) -> BFF (composition, shaping) -> services. Keep the gateway to edge concerns.

## Checked
2026-11-08. Confirmed against microservices.io API Gateway, Sam Newman's Backends For Frontends page (read via keyword search of the page, so only the matched passages were read) and the Microsoft Learn API gateway page. Removed (not stated on those pages): the product list (Kong, Envoy, Apigee and others), request size limits, CORS, canary routing, HA multi-AZ and latency-budget advice, GraphQL-per-frontend, and the pitfalls list.
Method: documentation only; no commands were run.
