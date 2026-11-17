---
id: computing-software.cloud-infrastructure-engineering.gateway-api.personas-and-rbac-write-permissions
name: personas-and-rbac-write-permissions
category: computing-software
field: cloud-infrastructure-engineering
product: gateway-api
tags: [rbac, personas, roles, ian, chihiro, ana, multi-tenancy]
level: practitioner
status: docs-checked
description: "Map Gateway API personas (infrastructure provider, cluster operator, application developer) onto Kubernetes RBAC write permissions for GatewayClass, Gateway and Routes."
sources:
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/docs/concepts/roles-and-personas.md
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/docs/concepts/security.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Personas: **Ian** (infrastructure provider), **Chihiro** (cluster operator), **Ana** (application developer). One human may hold several roles: a small startup may be all three, a typical small team merges Ana and Chihiro, and a large organisation splits them across groups.

Each persona is anticipated to map approximately to a Kubernetes RBAC `Role`. Write permissions for the simple three-tier model:

| | GatewayClass | Gateway | Route |
|---|---|---|---|
| Infrastructure Provider | Yes | Yes | Yes |
| Cluster Operators | No | Yes | Yes |
| Application Developers | No | No | Yes |

Advanced four-tier model adds Application Admins:

| | GatewayClass | Gateway | Route |
|---|---|---|---|
| Infrastructure Provider | Yes | Yes | Yes |
| Cluster Operators | Sometimes | Yes | Yes |
| Application Admins | No | In specified namespaces | In specified namespaces |
| Application Developers | No | No | In specified namespaces |

In most cases it is desirable for most roles to be able to read all resources, so the security page focuses on write access.

Ana's focus is the business needs of her application, not Kubernetes or Gateway API; from Gateway API's point of view she manages configuration (for example timeouts and request matching or filters) and Service composition (for example path routing to backends). Chihiro is concerned with policies, network access and application permissions; Ian is responsible for the infrastructure for multiple tenants, often at a cloud or PaaS provider.

The security page also says creating a Gateway should be treated as a privileged permission, because it can add cost and infrastructure changes such as a load balancer or DNS record, and that regular users should not be allowed to modify Gateway API status.

## Checked

2026-11-08. Read in full: the Roles and Personas page and the Security concept page (raw markdown on GitHub). Confirmed: the three personas and their pronouns and responsibilities, the three ways roles map to people (single user, small startup, large organisation), the approximate persona-to-Role mapping, both write-permission tables, and the Gateway creation and status permission guidance. Removed: the Ingress user split and the claims about what Ana and Chihiro can control through parentRefs, which are not on these pages.

Method: documentation only; no commands were run.
