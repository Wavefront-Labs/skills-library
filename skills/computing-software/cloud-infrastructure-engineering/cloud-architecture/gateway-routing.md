---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.gateway-routing
name: gateway-routing
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, api-gateway-patterns, gateway-routing, api-gateway, layer-7-routing, reverse-proxy, versioned-routing]
level: practitioner
status: docs-checked
description: "Expose many services, instances or versions behind one endpoint with layer 7 routing: when to use it, global vs regional gateways, and its failure and bottleneck risks."
sources: ["https://learn.microsoft.com/azure/architecture/patterns/gateway-routing"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Gateway routing

Place a gateway in front of a set of applications, services or deployments and use application layer 7 routing
to send each request to the right instances. The client knows about and talks to a single endpoint.

## When it helps (the three scenarios on the pattern page)
- **Multiple disparate services** (for example search, reviews, cart, checkout, order history): without a
  gateway the client must know every endpoint and change whenever an API changes or a service is split. With one,
  services can be consolidated, decomposed or replaced and only the routing changes.
- **Multiple instances of one service** (load balancing or availability, in one or several regions): the gateway
  encapsulates registering and unregistering instances as they scale, so the client is unaware.
- **Multiple versions of one service**, such as blue-green deployments: the gateway shifts the percentage of
  traffic to the new version without any client change.

## Use the pattern when
- A client needs several services behind one endpoint, or a variable number of instances, or services in
  multiple regions for latency or availability.
- You want to route externally addressable endpoints to internal virtual endpoints.
- You want clients to reach multiple versions of a service at the same time.
- You want to route traffic away from regions with high carbon emissions when lower-emission alternatives are in
  the backend pool.
It may not suit a simple application that uses only one or two services.

## Design considerations
- The gateway can be a single point of failure: design it for your availability requirements, with resiliency
  and fault tolerance.
- It can also be a bottleneck: size it for load and make sure it scales with growth. Load test it so it does not
  cause cascading failures for the services behind it.
- Routing is level 7 and can be based on IP, port, header or URL.
- Gateways can be global or regional. On Azure, Front Door is global and Application Gateway is regional. Use a
  global gateway for multi-region deployments; consider Application Gateway for a regional workload needing
  granular control of how traffic is balanced, such as between virtual machines.
- The gateway is the public endpoint for the services behind it, so consider making those services reachable
  only through the gateway or a private virtual network.

## Implementation options named on the page
- Application Gateway: regional layer 7 routing.
- Azure Front Door: global layer 7 routing.
- An Nginx example routes requests for applications under different virtual directories to different
  back-end machines.
Related patterns: Backends for Frontends, Gateway Aggregation, Gateway Offloading.

## Verify
- [ ] Clients use one endpoint and need no change when a service is split, merged or scaled.
- [ ] The gateway has been load tested and its availability design matches the workload's targets.

## Checked
2026-11-09. Confirmed against the Azure Architecture Center Gateway Routing page (body text read via grep of
paragraphs and list items; the Nginx configuration listing was not read line by line). Removed claims the page
does not make: route table, prefix versus host advice, longest-match precedence, Gateway API and API Gateway
specifics, the 29 second REST API timeout, gateway product comparison and CI route tests. The two other cited
sources were not read and were dropped.
Method: docs-checked 2026-11-09 against https://learn.microsoft.com/azure/architecture/patterns/gateway-routing; documentation only, no commands run.
