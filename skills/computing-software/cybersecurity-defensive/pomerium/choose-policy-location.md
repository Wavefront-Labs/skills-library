---
id: computing-software.cybersecurity-defensive.pomerium.choose-policy-location
name: choose-policy-location
category: computing-software
field: cybersecurity-defensive
product: pomerium
tags: [namespaces, clusters, route-policy, rbac-roles, policy-inheritance]
level: practitioner
status: docs-checked
description: "Decide where Pomerium policies live (routes, Enterprise namespaces, Zero clusters) and which policy language to use for each deployment size."
sources:
  - https://raw.githubusercontent.com/pomerium/documentation/main/content/docs/capabilities/authorization.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Pomerium re-evaluates user context (IdP claims, device posture, location) on every request.

Where policies live:
1. **Routes** (all editions): a policy per route controls who reaches the upstream.
2. **Namespaces** (Enterprise): a policy applied at a namespace is inherited by child namespaces and routes. Parents enforce global rules (for example a company email domain); children add local restrictions; team leads can manage their own routes. RBAC roles: Guest, Viewer, Manager, Admin.
3. **Clusters** (Zero): clusters pull routes, policies and certificates from the hosted control plane; policies are defined in the Zero console and synced to local Core replicas. Each cluster gets a starter domain with automatic TLS, replaceable with custom domains.

Recommended choice:
- Small setups: route-level policy in Core.
- Larger organisations: Namespaces (Enterprise).
- Multiple deployments: Clusters (Zero). Use a persistent file or PostgreSQL storage in production.

Language: use PPL (YAML) for most cases; Rego (Enterprise only) for advanced Open Policy Agent logic. Enterprise adds a visual Policy Builder and extra criteria such as time of day and external data records.

## Checked

2026-11-04. Confirmed against the Authorization page: where policies live, namespace inheritance and RBAC roles, Zero clusters and starter domain, planning guidance, PPL vs Rego, Enterprise Policy Builder. Nothing removed.

Method: documentation only; no commands were run.
