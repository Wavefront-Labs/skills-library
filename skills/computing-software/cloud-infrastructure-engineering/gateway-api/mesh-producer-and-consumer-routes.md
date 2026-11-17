---
id: computing-software.cloud-infrastructure-engineering.gateway-api.mesh-producer-and-consumer-routes
name: mesh-producer-and-consumer-routes
category: computing-software
field: cloud-infrastructure-engineering
product: gateway-api
tags: [gamma, mesh, producer-route, consumer-route, namespaces, httproute]
level: advanced
status: docs-checked
description: "Distinguish producer routes (same namespace as the Service) from consumer routes (other namespaces) in GAMMA, and how they scope who sees the configuration."
sources:
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/docs/mesh/gamma.md
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/docs/mesh/mesh-overview.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
In mesh mode the namespace of the Route relative to the target Service decides its scope.

- **Producer route**: created in the **same namespace as the Service**, typically by the Service owner. It is typically created by the workload's creator to define acceptable usage of the workload, and all requests from any client of the workload, from any namespace, are affected by it.
- **Consumer route**: created in a **different namespace** from the Service. It is meant to refine how a consumer makes requests of the workload, for example custom timeouts, and only affects requests from workloads in the same namespace as the Route. The page's example is an HTTPRoute in `fast-clients` with a Service parentRef (`name: smiley`, `namespace: faces`, `kind: Service`, `group: core`, `port: 80`) and `timeouts.request: 100ms`.

Limits: the page marks the relationship between producer and consumer routes as ongoing work. Multiple Routes for the same Service in a single namespace, producer or consumer, are combined by the Gateway API Route merging rules. It is therefore not currently possible to define distinct consumer routes for several consumers in one namespace: if `blender` and `mixer` both live in namespace `foodprep` and call the `oven` Service, they cannot set different timeouts with HTTPRoutes unless they are moved to separate namespaces.

## Checked

2026-11-08. Read in full: the Mesh overview and GAMMA Initiative pages (raw markdown on GitHub). Confirmed: producer route definition (same namespace, affects all clients from any namespace), consumer route definition (different namespace, affects only requests from the Route's namespace), the 100ms fast-clients example, merging of same-namespace Routes and the blender/mixer limitation, and the work-in-progress note. Removed: the precedence sentence, the blast-radius, status visibility and RBAC consequences, and the conformance report pointer, none of which are on the pages.

Method: documentation only; no commands were run.
