---
id: computing-software.cybersecurity-defensive.security-architecture.service-to-service-authentication
name: service-to-service-authentication
category: computing-software
field: cybersecurity-defensive
product: security-architecture
tags: [security-architecture, service-to-service-auth, mtls, workload-identity, oauth-client-credentials, spiffe, service-mesh]
level: advanced
status: docs-checked
description: "Design service-to-service authentication: mTLS with workload identity (SPIFFE, mesh), OAuth mTLS client auth and token exchange, avoiding shared static secrets."
sources:
  - https://spiffe.io/docs/latest/spiffe-about/overview/
  - https://www.rfc-editor.org/rfc/rfc8705.html
  - https://www.rfc-editor.org/rfc/rfc8693.html
  - https://istio.io/latest/docs/reference/config/security/peer_authentication/
  - https://istio.io/latest/docs/reference/config/security/authorization-policy/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Service-to-service authentication

**Goal:** every internal call proves which workload is calling, using short-lived,
automatically rotated credentials, and authorisation is enforced per service, not by
network location.

## Options
1. **mTLS with workload identities**
   - SPIFFE defines short-lived cryptographic identity documents (SVIDs, X.509 or JWT) that workloads use to authenticate to each other, for example by establishing a TLS connection. SPIRE, Istio and cert-manager are among the implementations that issue X.509 SVIDs.
   - Authorisation policy on the receiver by peer identity: in Istio, `AuthorizationPolicy` `principals` match the identity from the peer certificate (format `<TRUST_DOMAIN>/ns/<NAMESPACE>/sa/<SERVICE_ACCOUNT>`) and require mTLS; `serviceAccounts` is typically simpler.
2. **OAuth 2.0 mutual TLS (RFC 8705)**
   - Client authentication by mTLS to the authorisation server, and certificate-bound access tokens so a stolen token is unusable without the client's key. Prefer these (or `private_key_jwt`) over shared client secrets.
   - The receiving API validates the token signature, audience (`aud`), expiry (`exp`) and scopes.
3. **Token exchange (RFC 8693)** to obtain a new token for a downstream service (delegation or impersonation) instead of forwarding the user's original token everywhere.

## Design rules
- No shared API keys or passwords between services; if unavoidable, store in a secret
  manager with rotation and per-consumer keys.
- Validate audience: a token for service A must not be accepted by service B.
- Authorisation at the receiver: an Istio ALLOW policy with no matching rule denies; DENY policies should be scoped to a specific port, because missing attributes on TCP traffic count as matches.
- Propagate end-user identity separately from service identity when authorisation depends on both.
- Log caller identity on every request for investigations (Istio's AUDIT action logs requests without affecting allow or deny).

## Rollout in a mesh
Istio `PeerAuthentication` modes: PERMISSIVE accepts plaintext or mTLS, STRICT requires an mTLS tunnel, UNSET inherits from the parent (PERMISSIVE otherwise). Start PERMISSIVE, find the plaintext traffic, migrate, then STRICT per namespace; then add authorisation policies starting with critical services.

## Gotchas
- mTLS only authenticates; without authorisation policies any workload in the mesh can call anything.
- Long-lived certificates or tokens copied into config files defeat rotation.

## Verify
A test workload with a different service account is denied by a protected service; plaintext
requests are rejected in STRICT mode; logs show caller identity per request.

## Checked
Confirmed on the SPIFFE overview: short-lived SVIDs, TLS or JWT use, implementers (SPIRE, Cert-manager, Istio issue X.509 SVIDs). Confirmed on the Istio PeerAuthentication page: PERMISSIVE, STRICT, UNSET semantics. Confirmed on the Istio AuthorizationPolicy page: principals format and mTLS requirement, serviceAccounts, ALLOW with no rules, DENY and port scoping, AUDIT. RFC 8705 and RFC 8693 were downloaded and checked only for the topics (mTLS client authentication and certificate-bound tokens; token exchange with delegation and impersonation), not read line by line. Removed: the cloud-native identities item (AWS, Azure, GCP; no source), Linkerd, lifetimes in hours, the OAuth client credentials audience wording, the 403 test result, and the clock-skew note.
Method: docs-checked 2026-11-09 against the SPIFFE overview, Istio PeerAuthentication and AuthorizationPolicy reference pages, and RFCs 8705 and 8693 (topic-level grep).
