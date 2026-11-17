---
id: computing-software.cloud-infrastructure-engineering.gateway-api.ingress-to-gateway-concept-mapping
name: ingress-to-gateway-concept-mapping
category: computing-software
field: cloud-infrastructure-engineering
product: gateway-api
tags: [ingress, migration, gateway, httproute, annotations, concept-mapping]
level: intro
status: docs-checked
description: "Map Ingress concepts to Gateway API: entry points to Gateway listeners, rules to HTTPRoute, TLS secret to the listener, annotations to fields."
sources:
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/guides/getting-started/migrating-from-ingress.md
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/guides/getting-started/simple-gateway.md
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/docs/introduction/_index.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Mapping from the migration guide:

| Ingress | Gateway API |
|---|---|
| Ingress class (IngressClass) | HTTPRoute `parentRefs` select the Gateway to attach to; the Gateway's GatewayClass selects the implementation |
| Two implicit entry points (HTTP and HTTPS) from the controller | Entry points defined explicitly as Gateway listeners |
| `tls` section with a Secret | TLS termination is a property of the Gateway listener, with the certificate and key still in a Secret |
| `rules[].host` | HTTPRoute `hostnames`; rules apply to all hostnames of the route, not per host |
| path rules | HTTPRoute rules and path matches |
| default backend | no direct equivalent: define an explicit rule, for example prefix `/` to a Service |
| controller-specific annotations | typed features, or extension points (see below) |

Differences that matter:

- Personas: Ingress has one user persona; Gateway API splits it. The cluster operator or application admin owns Gateways (entry points and TLS termination), the application developer owns HTTPRoutes, and a single RBAC Role can still cover all three for a self-service model.
- The hostnames of an HTTPRoute must match the Gateway listener hostname, otherwise the listener ignores the unmatched ones.
- Features that needed annotations and are now part of HTTPRoute: request redirects (including TLS redirect), request/response manipulation, traffic splitting, and header, query-param or method-based routing.
- Merging of overlapping rules is prescribed: an implementation must merge the rules of all HTTPRoutes attached to a listener and resolve conflicts per the API design guide, whereas Ingress controllers each do it their own way.
- Extension points are external references (for example `extensionRef` on an HTTPRouteFilter), implementation-specific conformance levels, and Policies, which reference Gateway API resources; annotations on Gateway API resources are strongly discouraged.
- Gateway API is described as supporting all features of Ingress resources, and the ingress2gateway project helps convert Ingress to HTTPRoutes.

Not everything converts one to one; behaviour that came from custom annotations may need the implementation's own extension points.

## Checked

2026-11-08. Read in full (GitHub markdown): the Migrating from Ingress guide, the simple Gateway guide and the introduction. Confirmed: all table rows and the differences above. Removed: the claims that `tls[].secretName` maps to the literal field `tls.certificateRefs` (field name not stated on these pages), that Secrets are shared through ReferenceGrant, and the "Ingress has one class per resource" contrast (the guide only says an Ingress must name a class while an HTTPRoute names Gateways in parentRef). Rewrote the controller-to-Gateway row to match the guide's entry-point wording.

Method: documentation only; no commands were run.
