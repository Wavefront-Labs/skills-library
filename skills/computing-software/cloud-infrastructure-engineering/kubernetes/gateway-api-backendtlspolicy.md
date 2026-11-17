---
id: computing-software.cloud-infrastructure-engineering.kubernetes.gateway-api-backendtlspolicy
name: gateway-api-backendtlspolicy
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, gateway-api, backendtlspolicy, tls, backend-tls, mtls]
level: practitioner
status: docs-checked
description: "Encrypt Gateway-to-backend traffic with BackendTLSPolicy, pointing at a CA ConfigMap and the backend hostname, and debug its status."
sources: ["https://gateway-api.sigs.k8s.io/reference/api-types/policy/backendtlspolicy/", "https://gateway-api.sigs.k8s.io/guides/user-guides/backend-protocol/", "https://github.com/kubernetes-sigs/gateway-api/blob/main/apis/v1/backendtlspolicy_types.go"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# BackendTLSPolicy

By default a Gateway terminates TLS and talks plain HTTP to Services. BackendTLSPolicy makes the
Gateway originate TLS to the backend and verify its certificate.

```yaml
apiVersion: gateway.networking.k8s.io/v1      # GA, Standard channel since Gateway API v1.4.0
kind: BackendTLSPolicy
metadata: {name: payments-tls, namespace: shop}
spec:
  targetRefs:
  - group: ""
    kind: Service
    name: payments
    sectionName: https          # optional: one Service port by name
  validation:
    caCertificateRefs:
    - group: ""
      kind: ConfigMap
      name: internal-ca          # key ca.crt
    hostname: payments.shop.svc.cluster.local
```
Use `wellKnownCACertificates: System` instead of `caCertificateRefs` for public certificates (only one
of the two may be set). The core-supported CA reference is a single ConfigMap with the certificate in the
key `ca.crt`, in the policy's own namespace (cross-namespace certificate references are not allowed).
The `hostname` is the SNI the Gateway uses and must match the certificate the backend serves (no IPs or
wildcards); optional `subjectAltNames` separates certificate identity from SNI.

## Notes
- Check that your implementation supports it and which version (`kubectl get crd
  backendtlspolicies.gateway.networking.k8s.io`).
- The HTTPRoute is unchanged; it still references the Service port. The policy applies to routes that
  forward to the targeted Service, including GRPCRoute and TLSRoute in Terminate mode.

## Debug
```bash
kubectl describe backendtlspolicy payments-tls -n shop    # status.ancestors[].conditions Accepted
```
A bad CA reference sets `ResolvedRefs=False` with reason `InvalidCACertificateRef` (missing object or no
`ca.crt` key) or `InvalidKind`; if every reference is invalid, `Accepted=False` with reason
`NoValidCACertificate`. Connections using an invalid reference must fail with an HTTP 5xx. Failures
after enabling usually mean a hostname mismatch or the backend serving plain HTTP on that port.

## Verify
Backend access logs show TLS connections from the gateway, and a backend with a wrong cert gets
rejected (5xx to the client) instead of accepted.

## Checked

Documentation release: Gateway API docs (kubernetes-sigs/gateway-api site/content and apis/v1, latest release v1.6.3, repo commit 2026-10-23; v1.7.0 is at release-candidate stage).
Confirmed against the BackendTLSPolicy page and apis/v1 types: Standard channel since v1.4.0 (`v1`), `targetRefs` with `sectionName`, `validation.caCertificateRefs` vs `wellKnownCACertificates: System` (mutually exclusive), `hostname` as SNI (no wildcards or IPs), `subjectAltNames`, ConfigMap key `ca.crt`, cross-namespace certificate refs disallowed, `status.ancestors` conditions, reasons `InvalidCACertificateRef`, `InvalidKind`, `NoValidCACertificate`, and 5xx on failure.
Corrected: the condition and reason pairing in the debug section, the exact 503 claim and the SAN claim. Removed the unsourced trust-manager note.

Method: documentation only; no commands were run.
