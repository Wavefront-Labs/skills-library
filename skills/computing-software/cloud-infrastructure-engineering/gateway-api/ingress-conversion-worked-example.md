---
id: computing-software.cloud-infrastructure-engineering.gateway-api.ingress-conversion-worked-example
name: ingress-conversion-worked-example
category: computing-software
field: cloud-infrastructure-engineering
product: gateway-api
tags: [ingress, migration, tls-redirect, httproute, gateway, foo-bar]
level: practitioner
status: docs-checked
description: "Worked Ingress to Gateway API conversion: one Gateway with http and https listeners, foo and bar HTTPRoutes, and a TLS redirect route."
sources:
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/guides/getting-started/migrating-from-ingress.md
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/guides/user-guides/http-redirect-rewrite.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The migration guide converts one Ingress (IngressClass `prod`) that terminated TLS for `foo.example.com` and `bar.example.com` with the Secret `example-com`, routed `foo` paths `/` and `/orders` to two Services and `bar` to one Service, and issued a TLS redirect through a controller-specific annotation (`example-ingress-controller.example.org/tls-redirect`).

Result, in three steps:

1. **Gateway** (GatewayClass `prod`): an `http` listener on port 80 and an `https` listener on port 443 terminating TLS with the same Secret. Both allow HTTPRoutes from the same namespace (the default) and restrict hostnames to the `example.com` subdomain.
2. **foo and bar HTTPRoutes**: the Ingress is split into one HTTPRoute per hostname, attached to the `https` listener, with the same routing rules as the Ingress rules for that host. In an HTTPRoute the rules apply to all its hostnames, whereas an Ingress has separate rules per host; this is why the guide splits by host. HTTPRoutes are owned by the application developer.
3. **Redirect HTTPRoute**: attached to the `http` listener (set `sectionName` to the listener name `http`) with a `RequestRedirect` filter, `scheme: https` and `statusCode: 301`, for the foo and bar hostnames. It replaces the annotation. Redirects change only the configured URL components and preserve the rest (host, path, port).

Notes from the guides:

- A Route needs an HTTPS listener whose Secret is referenced in `certificateRefs`; the HTTPRoute hostnames must match the listener hostname or the listener ignores the unmatched ones.
- The default 302 applies if `statusCode` is not set; 301, 302, 303, 307 and 308 are supported (303, 307 and 308 are extended features).
- Redirect and URLRewrite filters cannot be combined on one rule.
- The Ingress default backend has no direct equivalent: define an explicit rule, for example prefix `/` to a Service.
- Anything the old controller did through other annotations needs its own mapping; consult your Gateway implementation's docs. The `ingress2gateway` tool can convert Ingresses to HTTPRoutes, and its results should always be tested and verified.

## Checked

2026-11-08. Read in full (GitHub markdown): the Migrating from Ingress guide and the HTTP redirects and rewrites guide. Confirmed: the three-part structure, listener ports, route splitting reason, redirect scheme and 301, sectionName attachment, default 302 and supported codes, filter incompatibility, default backend note, ingress2gateway caveat. Example YAML files are Hugo includes and were not visible, so field spellings come only from the prose. Removed: `tls.mode: Terminate` wording, the Programmed/Accepted/ResolvedRefs sequence and the DNS cutover steps (not in these pages).

Method: documentation only; no commands were run.
