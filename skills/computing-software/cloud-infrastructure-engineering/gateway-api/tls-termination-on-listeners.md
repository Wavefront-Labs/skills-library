---
id: computing-software.cloud-infrastructure-engineering.gateway-api.tls-termination-on-listeners
name: tls-termination-on-listeners
category: computing-software
field: cloud-infrastructure-engineering
product: gateway-api
tags: [tls, termination, listener, https, certificaterefs, secret]
level: practitioner
status: docs-checked
description: "Terminate TLS at a Gateway listener: protocol HTTPS, tls.mode Terminate, certificateRefs to Secrets, and the difference between Terminate and Passthrough."
sources:
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/guides/user-guides/tls.md
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/reference/api-types/gateway.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Downstream TLS is configured per listener in `Gateway.spec.listeners[].tls`.

- `mode: Terminate`: the Gateway decrypts and then routes. By listener protocol: HTTPS with HTTPRoute, GRPC with GRPCRoute, TLS with TLSRoute (Terminate is Extended for TLSRoute).
- `mode: Passthrough` (protocol TLS, TLSRoute): the TLS session is not terminated at the Gateway, so TLS settings do not take effect and the encrypted stream is routed.
- `certificateRefs`: references to Kubernetes Secrets holding the server certificate and key, used for Terminate.

```yaml
listeners:
- name: https
  protocol: HTTPS
  port: 443
  hostname: "foo.example.com"
  tls:
    mode: Terminate
    certificateRefs:
    - name: foo-example-com-cert
```

A certificate in another namespace is allowed by a ReferenceGrant created in the target namespace; without it the cross-namespace reference is invalid.

TLS settings of a listener apply to all domains that satisfy its `hostname`. With a wildcard listener certificate for `*.example.com` and a different one for `foo.example.com`, the specific match takes priority, so the Gateway serves the specific certificate for `foo.example.com` and the wildcard one for other requests.

The TLS guide also shows an `options` map for implementation-specific TLS settings. The `options` map is for implementation-specific features such as TLS version restrictions or ciphers, so check your implementation's TLS documentation.

Gateway status reports `Addresses`, per-listener `Listeners` status and `Conditions`; check these when a spec cannot be achieved.

## Checked

2026-11-08. Read in full: the TLS configuration guide and the Gateway reference (raw markdown on GitHub). Confirmed: listener-level tls with mode Terminate or Passthrough and certificateRefs to Secrets, the protocol/mode/route-type table, Passthrough ignoring TLS settings, ReferenceGrant for cross-namespace certificates, hostname scoping and wildcard-versus-specific certificate priority, the options map, and Gateway status fields. Removed: Terminate being the default for HTTPS listeners, the same-namespace permission statement, the claim that distinct listeners on a port must differ, hostname intersection with Routes, and the ResolvedRefs and Programmed condition names. The listener YAML is a condensed sketch.

Method: documentation only; no commands were run.
