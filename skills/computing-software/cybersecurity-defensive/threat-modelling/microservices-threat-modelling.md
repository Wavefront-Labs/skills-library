---
id: computing-software.cybersecurity-defensive.threat-modelling.microservices-threat-modelling
name: microservices-threat-modelling
category: computing-software
field: cybersecurity-defensive
product: threat-modelling
tags: [microservices-threat-modelling, microservices-security, mtls, service-to-service-auth, token-validation, logging]
level: advanced
status: docs-checked
description: "Threat model microservices using the OWASP Microservices Security Cheat Sheet: edge vs service authorisation, identity propagation, mTLS vs tokens, logging pipeline."
sources: ["https://raw.githubusercontent.com/OWASP/CheatSheetSeries/master/cheatsheets/Microservices_Security_Cheat_Sheet.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Microservices threat modelling

The cheat sheet treats authentication and authorisation as the fundamental security
requirements to settle at design time in a microservices system. Use these as the question
set when drawing the data flow diagram and its trust boundaries.

## Authorisation threats
- **Edge-level only**: gateway checks should reject unauthorised ingress requests and
  prevent direct access that bypasses them. Fine-grained authorisation stays at the service
  when it needs resource or business context.
- **Service-level**: each service must enforce access to its protected operations, including
  internal calls. Gateway checks complement this; they do not establish that a downstream
  operation is authorised. The sheet prefers shared, reviewed policies as the system grows,
  with service-level enforcement of object, tenant and business-specific rules.

## Identity propagation
Propagate authenticated user context in a form each receiving service can validate, and
authenticate the calling service separately. A signature protects an assertion's integrity;
it does not grant access to a requested resource.

## Service-to-service authentication
- **Mutual TLS**: each service carries a key pair and authenticates to recipients, giving
  mutual identification plus confidentiality and integrity. Usually runs on a self-hosted
  PKI. Main challenges: key provisioning and trust bootstrap, certificate revocation, key
  rotation.
- **Token-based**: a signed token (caller ID and permissions or scopes) obtained from a
  security token service is attached to each request, for example in HTTP headers, and the
  called service validates it online or offline. It normally runs over TLS.
  - Online validation (OAuth token introspection) can reflect revocation but adds latency and
    a dependency on the token service. Caching introspection responses delays detection of
    revocation, so bound cache duration to the required freshness and never beyond token
    expiry.
  - Local validation of a signed token against trusted issuer keys avoids a per-request call
    but does not detect server-side revocation before expiry. Signature verification alone is
    insufficient (the sheet points to RFC 9068 for JWT access token validation). Use token
    lifetimes or another revocation mechanism that meets the response time you need.
  - Neither approach replaces service-level authorisation. Reject requests when required token
    validation cannot be completed.

## Logging pipeline threats
The sheet's pattern is: services write to stdout or stderr, a local agent publishes to a
message broker, and a central logging service subscribes.
- Local buffering does not guarantee lossless delivery (storage limits, rotation, node loss);
  a broker alone does not prevent log loss or denial of service. Define buffer limits and
  behaviour when storage fills, monitor delivery failures and test recovery.
- Agent and broker should use mutual authentication (for example TLS) to mitigate service
  spoofing, logging-system spoofing, traffic injection and sniffing.
- The broker should enforce access control with least privilege, mitigating service elevation
  of privilege.
- Exclude secrets and unnecessary sensitive data before the service emits a log entry;
  agent-side filtering cannot remove data already written locally.
- Generate a correlation ID per call chain and include it in every log message; publish
  structured logs with platform and runtime context.

## Verify
- [ ] The DFD shows where each call is authenticated and where authorisation is enforced.
- [ ] Token validation mode (online or local) was chosen against revocation response time.
- [ ] Logs carry correlation IDs and exclude secrets.

## Checked
Confirmed 2026-11-09 against the OWASP Microservices Security Cheat Sheet (raw markdown, read in full).
Removed as unconfirmed: SPIFFE IDs, Istio, Linkerd and Consul references, RFC 8693 token exchange, the confused-deputy, async-messaging, data-ownership, NetworkPolicy and egress allowlist items, circuit breaker and observability-leakage claims, the mesh permissive-mode and actuator-endpoint gotchas, and the NIST SP 800-204 and 800-204A sources, which were not read.
Method: docs-checked 2026-11-09 against raw.githubusercontent.com OWASP CheatSheetSeries Microservices_Security_Cheat_Sheet.md
