---
id: computing-software.cloud-infrastructure-engineering.gateway-api.service-facets-routing-vs-endpoint-routing
name: service-facets-routing-vs-endpoint-routing
category: computing-software
field: cloud-infrastructure-engineering
product: gateway-api
tags: [gamma, service, service-facets, frontend, backend, endpoint-routing]
level: advanced
status: docs-checked
description: "Understand Service facets in Gateway API: the frontend facet (cluster IP, DNS name) versus the backend facet (endpoints), and service routing versus endpoint routing."
sources:
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/docs/mesh/service-facets.md
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/docs/mesh/gamma.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The service-facets page separates a Kubernetes Service into two roles, because Gateway API uses it both as a target and as a destination.

- **Frontend facet**: the Service as a name clients call, with its cluster IP and DNS name. The facet matters for GAMMA mesh work, because the gateway and the mesh each decide whether a request that mentions a Service is directed to its frontend or its backend.
- **Backend facet**: the Service as a set of endpoints that traffic can be sent to. Pods are not part of the backend facet, though they are strongly associated with the endpoint IPs.

Routing styles that follow:

- **Service routing**: the Route sends to the Service and lets the platform (kube-proxy or the mesh) choose an endpoint. Which endpoint is used is left to the underlying network infrastructure.
- **Endpoint routing**: the request is directed to the Service's endpoint IPs, which is often necessary for more advanced load balancing decisions, for example a gateway implementing sticky sessions.

The page says Service routing may be the most direct fit for the application developer persona's sense of routing, while endpoint routing can be more predictable when Gateway API is used for both north/south and east/west traffic; GAMMA is working to formalize guidance. When something behaves differently between implementations, check which style each uses.

## Checked

2026-11-08. Read in full: the Service Facets page and the GAMMA Initiative page (raw markdown on GitHub). Confirmed: the frontend facet is the cluster IP plus DNS name, the backend facet is the endpoint IPs (not the Pods), Service routing leaves endpoint choice to kube-proxy, a mesh or other infrastructure, and endpoint routing enables advanced load balancing such as sticky sessions. Removed: the claim that parentRefs or backendRefs map to a facet, the list of behaviour differences and the weighted subsets, retries and session persistence list, none of which are on the pages.

Method: documentation only; no commands were run.
