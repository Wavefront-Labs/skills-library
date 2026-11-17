---
id: computing-software.cloud-infrastructure-engineering.gateway-api.ingress-nginx-migration-and-ingress2gateway
name: ingress-nginx-migration-and-ingress2gateway
category: computing-software
field: cloud-infrastructure-engineering
product: gateway-api
tags: [ingress-nginx, ingress2gateway, migration, annotations, tooling, cors]
level: practitioner
status: docs-checked
description: "Plan a migration off ingress-nginx using ingress2gateway and Gateway API features: what is native, what needs implementation policy."
sources:
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/guides/getting-started/migrating-from-ingress-nginx.md
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/docs/concepts/tooling.md
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/guides/getting-started/migrating-from-ingress.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The Ingress-NGINX welcome guide splits what Ingress combines: a Gateway defines where and how traffic enters the cluster (cluster operator) and an HTTPRoute defines routing to Services (application developer).

`ingress2gateway` (a SIG-Network subproject) reads existing Ingress resources and converts them to Gateway and HTTPRoute resources. It is under active development, with ongoing work to support the most widely used Ingress-NGINX annotations, and the guide recommends it as the starting point. The general migration guide adds that conversion results should always be tested and verified.

Approach drawn from the guides:

1. Choose an implementation first. Check its conformance reports for the Gateway API features you need, weigh your team's familiarity with its proxy (Envoy, NGINX and others) and whether your cloud provider or CNI already offers one.
2. Run a Gateway API controller alongside Ingress-NGINX: each gets a different external IP address, so you can test the new configuration without affecting production traffic.
3. Map annotations: traffic splitting, header manipulation and TLS configuration are native to Gateway API. The Ingress migration guide lists request redirects (including TLS redirect), request/response manipulation, traffic splitting and header, query-param or method-based routing as now part of HTTPRoute. Remaining features, such as authentication and non-portable data-plane settings, rely on extension points of your implementation (filters via `extensionRef`, policy resources).

Roadmap in the guide: the next release (then targeting February) hoped to graduate TLSRoute, ListenerSet and the HTTPRoute CORS filter to GA. Check current release notes before relying on them.

Tooling page: `gwctl` is a command line tool for exploring policies and xRoutes, and Headlamp is a Kubernetes UI with built-in Gateway API support (map view and tables, updated in real time).

## Checked

2026-11-08. Read in full (GitHub markdown): the Ingress-NGINX welcome guide, the Tooling page and the Migrating from Ingress guide. Confirmed: ingress2gateway description and status, side-by-side testing with different IPs, implementation selection factors, native feature examples, graduation targets, gwctl and Headlamp. Removed: the claim that the converter reports what it could not translate, rate limiting and custom snippets wording, and the specific claim that timeouts and retries are route fields (not on these pages).
Method: documentation only; no commands were run.
