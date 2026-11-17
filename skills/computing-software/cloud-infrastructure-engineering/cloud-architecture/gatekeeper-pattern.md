---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.gatekeeper-pattern
name: gatekeeper-pattern
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, design-patterns-cloud, gatekeeper-pattern, gatekeeper, request-validation, broker-host, trusted-host, security-pattern]
level: practitioner
status: docs-checked
description: "Protect sensitive services with a gatekeeper: a limited-privilege broker that validates and sanitises requests and holds no keys, in front of a trusted host that does."
sources: ["https://learn.microsoft.com/azure/architecture/patterns/gatekeeper"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Gatekeeper

A dedicated component brokers requests between clients and the application, validating and sanitising them, adding a
security layer and limiting attack surface. Decouple the code that implements public endpoints from the code that
processes requests and accesses storage.

## Structure
- **Gatekeeper** (public-facing): validates all requests and rejects those that fail; may authorize, look for
  unexpected or invalid payload content, and rate limit. Runs in limited-privilege mode and does **not** have the
  credentials or keys the trusted host uses, so a compromise cannot directly reach the services or data. It should do
  no application processing and no data access.
- **Trusted host / key master** (private): does the actual work with access to services and storage. It exposes only
  internal or protected endpoints used by the gatekeeper, never external ones. It may add extra validation, but the
  gatekeeper does the core validation.
- Like a network firewall, but application-aware: it can examine requests in detail and decide per request.

## When
Sensitive information, services needing strong protection from malicious traffic, mission-critical operations that
cannot tolerate direct back-end exposure, or a need to separate validation from business processing. Not suited when
built-in platform controls on the back end already meet the requirements, or when extra hops and validation latency
break strict end-to-end latency needs.

## Design steps
1. Host the gatekeeper and trusted back end on separate compute boundaries; keep back-end endpoints private.
2. Use HTTPS/TLS between gatekeeper and trusted host where possible (some hosting environments do not support HTTPS on
   internal endpoints).
3. Throttle at the gatekeeper instead of coordinating rate state across every node.
4. Run redundant instances with autoscaling: the gatekeeper can be a single point of failure.
5. Centralise logs and metrics from each layer and propagate a correlation ID from the edge.

## Azure layered example
Application Gateway with Web Application Firewall is the outer gatekeeper (WAF can block SQL injection and
cross-site scripting patterns, enforce protocol and request-size rules, bot and IP filtering); API Management is the
inner gatekeeper (JWT validation, rate limiting, header transformation) and forwards only approved traffic to a
private back end such as App Service behind a private endpoint, authenticating with managed identity. For containers,
AKS or Container Apps ingress can replace the inner path while keeping the same boundaries.

## Gotchas
- A gatekeeper that forwards requests unvalidated is just a proxy.
- Extra processing and network hops affect performance.

## Verify
- [ ] Back-end endpoints are reachable only through the gatekeeper path.
- [ ] A simulated compromise of the gatekeeper yields no credentials or data-store access.

## Checked
2026-11-08. Confirmed against the Azure Architecture Center Gatekeeper pattern page: structure, limited privilege,
no keys at the gatekeeper, private trusted host, TLS where supported, throttling, SPoF and redundancy, performance
cost, when to use or avoid, layered Application Gateway/WAF and API Management example. Removed as not stated there:
mTLS, schema/size-limit/canonicalisation detail, NSG rules, and the OWASP Top 10 source (it supports no claim in the
skill).
Method: documentation only; no commands were run.
