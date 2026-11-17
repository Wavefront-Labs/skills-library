---
id: computing-software.cloud-infrastructure-engineering.contour.contour-extensionservice-for-ext-authz
name: contour-extensionservice-for-ext-authz
category: computing-software
field: cloud-infrastructure-engineering
product: contour
tags: [extensionservice, ext-authz, grpc, protocol-h2, validation, loadbalancerpolicy, checkrequest-v3]
level: advanced
status: docs-checked
description: "ExtensionService CRD for external authorization: same-namespace rule, weighted services, h2 default, TLS validation of the auth server, Envoy v3 CheckRequest requirement."
sources: ["https://github.com/projectcontour/contour/blob/main/site/content/docs/main/config/client-authorization.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# ExtensionService for external authorization

Envoy's ext_authz filter holds a request, sends a check to an external gRPC server, and allows, denies or redirects. Contour binds that server with an `ExtensionService` (`projectcontour.io/v1alpha1`).

```yaml
apiVersion: projectcontour.io/v1alpha1
kind: ExtensionService
metadata:
  name: htpasswd
  namespace: projectcontour-auth
spec:
  protocol: h2
  services:
  - name: htpasswd
    port: 9443
    weight: 100
  loadBalancerPolicy:
    strategy: RoundRobin
  validation:
    caSecret: auth-ca
    subjectName: htpasswd.projectcontour-auth
```

Rules:
- The server must implement Envoy's `CheckRequest` gRPC protocol, version v3.
- The ExtensionService must be in the same namespace as the Services it targets (`spec.services[].name`), so one party controls both.
- Several Services can be listed; requests split by `weight`, useful for blue-green moves. `loadBalancerPolicy` governs endpoints inside each Service.
- `protocol` defaults to `h2`, HTTP/2 over TLS. Always set `validation` (expected server name plus trusted CA bundle) in production, otherwise credentials could go to an imposter service.
- In principle the Envoy cluster that an ExtensionService creates can be used for any purpose; the page covers only its use as an authorization service.

The manifest values above (names, port 9443, weight, strategy) are illustrative.

## Checked

2026-11-08. Read the Contour main-branch config page client-authorization.md in full. Confirmed: ext_authz behaviour, the ExtensionService API, gRPC CheckRequest with the v3 requirement, `.spec.services` and the same-namespace rule, weights for proportional splitting and blue-green use, `.spec.loadBalancerPolicy`, the `h2` default for `.spec.protocol`, and `.spec.validation` (expected server name plus trusted CA bundle). Removed the claim that the same CRD serves the global rate limit service. Example field values other than those named above are illustrative and not taken from the page.

Method: documentation only; no commands were run.
