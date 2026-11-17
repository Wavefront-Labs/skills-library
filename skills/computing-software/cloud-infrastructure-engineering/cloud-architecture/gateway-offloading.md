---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.gateway-offloading
name: gateway-offloading
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, api-gateway-patterns, gateway-offloading, tls-termination, authentication-offload, waf, throttling, trust-boundary]
level: practitioner
status: docs-checked
description: "Move shared cross-cutting work (TLS, authentication, throttling, monitoring) to a gateway while preventing bypass, re-encrypting to backends and keeping business logic out."
sources: ["https://learn.microsoft.com/azure/architecture/patterns/gateway-offloading"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Gateway offloading

Offload shared or specialised functionality to a gateway proxy so it is configured once instead of
duplicated across services. The gateway handles cross-cutting concerns such as client-facing certificate
management, authentication, TLS termination, monitoring, protocol translation and throttling for the backends.

## Good candidates
- Client-facing TLS certificate termination and its expiry tracking, which otherwise must be updated, tested and
  verified on every application instance.
- Authentication, authorisation checks that are common to services, logging, monitoring and throttling.
- Static old-to-new URL redirects, which the gateway can answer without invoking a backend. Match only the
  intended legacy URLs; keep redirects that depend on business state or application-specific authorisation in the
  application.
- Consistent request and response logging, giving a baseline of monitoring even for a poorly instrumented service.

## Never offload
Business logic. Do not tightly couple service-specific logic or routing to the gateway, or backend updates will
force gateway redeployment.

## Trust boundary
1. Backends must accept requests only through the intended gateway path. Otherwise clients connect directly and
   bypass authentication, throttling, request inspection and logging.
2. Decide whether each backend authorises the original caller, the gateway's workload identity or both. Preserve
   caller tokens or trusted claims only when the backend needs delegated user context. Authenticate the gateway to
   the backend separately, and do not treat unverified forwarded headers as proof of identity.
3. If the gateway terminates TLS, re-establish TLS to the backend. Do not forward over plain HTTP; treat all networks
   as untrusted. You still need a process to issue, rotate and revoke backend certificates.

## Design considerations
- High availability: run multiple gateway instances. It terminates client connections and can buffer request
  bodies, so use connection draining or graceful shutdown to avoid dropping active sessions.
- Capacity: provision for peak bursts, not average load; under-provisioning degrades every service behind it.
- Generate correlation IDs if you need to track transactions.
- The gateway concentrates operational responsibility (configuration, certificate lifecycle, policy updates,
  version upgrades) and is a high-value target, so harden it, restrict its management surface and monitor it
  independently of the backends.
- Not suitable when the concern is lightweight and the workload latency-sensitive (extra hop), or when the
  gateway team's release cycle is slower than the service teams' and becomes a change-management bottleneck.

## Azure example from the page
Application Gateway WAF_v2: an HTTPS listener on port 443, a PFX certificate sourced from Key Vault, a backend
pool of HTTPS servers (VMs, scale sets, IPs or App Service) with access restricted so clients cannot bypass the
gateway and its WAF policy, backend HTTP settings with HTTPS, certificate trust and a matching hostname (a trusted
root certificate for a private CA), a routing rule, and a WAF policy of managed and custom rules.

## Verify
- [ ] A direct call to a backend outside the gateway path fails.
- [ ] Traffic from the gateway to the backend is re-encrypted with certificates that are rotated.
- [ ] The gateway has a defined owner and team capacity for its configuration and certificate lifecycle.

## Checked
2026-11-09. Confirmed against the Azure Architecture Center Gateway Offloading page (body text read by extracting
paragraphs and list items). Removed claims not on the page and sources not read: the APIM validate-jwt and AWS
JWT authorizer pages, JWKS caching, X-Forwarded-For and PROXY protocol advice, spoofed X-User-Id header
stripping, CORS, compression and schema validation as offload candidates, and policy-as-code tests.
Method: docs-checked 2026-11-09 against https://learn.microsoft.com/azure/architecture/patterns/gateway-offloading; documentation only, no commands run.
