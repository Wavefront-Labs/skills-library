---
id: computing-software.cybersecurity-defensive.security-architecture.microservices-security
name: microservices-security
category: computing-software
field: cybersecurity-defensive
product: security-architecture
tags: [microservices-security, service-mesh, mtls, api-gateway, zero-trust, spiffe, authorization-policy, token-exchange]
level: advanced
status: draft
description: "Secure microservices: edge vs service-level auth, mTLS identity via mesh/SPIFFE, per-service authorization policy, token propagation and exchange, secrets and blast radius."
sources: ["https://csrc.nist.gov/pubs/sp/800/204/final", "https://cheatsheetseries.owasp.org/cheatsheets/Microservices_Security_Cheat_Sheet.html", "https://istio.io/latest/docs/concepts/security/", "https://datatracker.ietf.org/doc/html/rfc8693"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Microservices security patterns

## Layers
| Concern | Pattern |
|---|---|
| North-south authn | API gateway validates the user token (OIDC JWT) at the edge |
| Service identity | mTLS with workload identities (SPIFFE IDs, Istio/Linkerd certificates), never shared API keys |
| East-west authz | Per-service allow-lists: Istio `AuthorizationPolicy` / Linkerd `AuthorizationPolicy` - deny by default |
| User context | Propagate a token downstream; prefer token exchange (RFC 8693) to a narrowly scoped internal token over forwarding the external access token |
| Fine-grained authz | In the service (or OPA sidecar) - the gateway cannot know object ownership |
| Secrets | Per-service secrets from a vault; no shared DB credentials across services |

## Istio deny-by-default
```yaml
apiVersion: security.istio.io/v1
kind: AuthorizationPolicy
metadata: {name: allow-nothing, namespace: payments}
spec: {}
---
apiVersion: security.istio.io/v1
kind: AuthorizationPolicy
metadata: {name: orders-to-payments, namespace: payments}
spec:
  selector: {matchLabels: {app: payments}}
  action: ALLOW
  rules:
  - from: [{source: {principals: ["cluster.local/ns/orders/sa/orders"]}}]
    to: [{operation: {methods: ["POST"], paths: ["/v1/charge"]}}]
```
Set `PeerAuthentication` mode `STRICT` so plaintext is refused.

## Gotchas
- Trusting "internal" calls because they come from inside the cluster is the classic failure; one compromised pod reaches everything.
- Forwarding the user's external token everywhere spreads a high-value bearer token; exchange or down-scope it.
- Validate JWTs in each service that makes authz decisions (signature, `aud`, `exp`) - not just at the gateway.
- Log the caller principal and user subject on every service for traceability.

## Verify
- [ ] A pod in an unrelated namespace gets 403 (RBAC: access denied) calling payments.
- [ ] Plaintext request to a STRICT namespace fails.
- [ ] Each service's authz decisions appear in logs with principal.
