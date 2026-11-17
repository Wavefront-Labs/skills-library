---
id: computing-software.software-engineering.software-architecture.deployment-and-runtime-views
name: deployment-and-runtime-views
category: computing-software
field: software-engineering
product: software-architecture
tags: [software-architecture, architecture-description, deployment-view, runtime-view, sequence-diagrams, arc42]
level: practitioner
status: draft
description: "Document deployment views (nodes, environments, networks, scaling) and runtime views (key scenarios as sequence diagrams) per arc42 sections 6-7 and C4 deployment diagrams."
sources: ["https://docs.arc42.org/section-6/", "https://docs.arc42.org/section-7/", "https://c4model.com/diagrams/deployment", "https://mermaid.js.org/syntax/sequenceDiagram.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Deployment and runtime views

## Runtime view (arc42 section 6)
Shows how building blocks collaborate in a few **important scenarios**: the main user journey,
startup, error/failover paths, a tricky integration. 3-6 scenarios, not every use case.

```mermaid
sequenceDiagram
  participant M as Mobile app
  participant G as API gateway
  participant O as Order service
  participant P as Payment provider
  M->>G: POST /orders (Idempotency-Key)
  G->>O: create order
  O->>P: authorize payment (2s timeout)
  P-->>O: authorized
  O-->>G: 201 Created
  G-->>M: 201 + order
  Note over O,P: on timeout -> order PENDING, reconcile job polls provider
```
Include timeouts, async hops (queues), and failure branches; that's where reviewers find bugs.

## Deployment view (arc42 section 7, C4 deployment diagram)
Maps software to infrastructure:
- Environments (prod, staging), regions/AZs, clusters, nodes or managed services.
- Which containers/services run where, replica counts and autoscaling bounds.
- Network zones, ingress/egress, load balancers, firewalls, private links.
- Data stores with replication and backup locations (data residency questions live here).
- Level 1 overview + level 2 details per environment if they differ.

Diagram-as-code: Structurizr DSL `deploymentEnvironment "Production" { deploymentNode "eu-west-1" {...} }`,
or Mermaid/PlantUML; generate infra parts from Terraform state where possible (inframap, Cloudcraft).

## Keep them true
- Store with the code; review in PRs that change infra or main flows.
- Each diagram has a title, key/legend, and date or version.
- Note what the view deliberately omits.
