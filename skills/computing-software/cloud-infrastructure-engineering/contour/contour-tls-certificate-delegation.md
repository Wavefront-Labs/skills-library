---
id: computing-software.cloud-infrastructure-engineering.contour.contour-tls-certificate-delegation
name: contour-tls-certificate-delegation
category: computing-software
field: cloud-infrastructure-engineering
product: contour
tags: [tlscertificatedelegation, wildcard-certificate, targetnamespaces, cross-namespace, tls-cert-namespace, ingress-annotation]
level: practitioner
status: docs-checked
description: "TLSCertificateDelegation: letting namespaces reference a Secret from another namespace for HTTPProxy and Ingress v1, targetNamespaces wildcard, tls-cert-namespace annotation."
sources: ["https://github.com/projectcontour/contour/blob/main/site/content/docs/main/config/tls-delegation.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# TLS certificate delegation

Delegation lets a certificate owner (for example holding a `*.example.com` Secret in an admin namespace) grant Contour permission to read that Secret for objects in other namespaces. It works for HTTPProxy and Ingress, but Ingress v1 needs an annotation.

```yaml
apiVersion: projectcontour.io/v1
kind: TLSCertificateDelegation
metadata:
  name: example-com-wildcard
  namespace: www-admin
spec:
  delegations:
  - secretName: example-com-wildcard
    targetNamespaces: [example-com]
  - secretName: another-com-wildcard
    targetNamespaces: ["*"]
```

Each delegation references a `secretName` from the namespace where the `TLSCertificateDelegation` is created and lists `targetNamespaces` in which the certificate can be referenced; `"*"` allows all namespaces.

Consume it from an HTTPProxy (or Ingress v1beta1) with slash syntax:

```yaml
tls:
  secretName: www-admin/example-com-wildcard
```

From Ingress v1, keep `spec.tls[].secretName: example-com-wildcard` and add the annotation `projectcontour.io/tls-cert-namespace: www-admin`.

If the `--watch-namespaces` flag is used, it must define all namespaces that will be referenced by the delegation.

## Checked

2026-11-08. Read the Contour main-branch config page tls-delegation.md in full. Confirmed: purpose, HTTPProxy and Ingress support, the Ingress v1 annotation, the resource shape, `"*"` target, slash syntax and the `--watch-namespaces` requirement. Removed the closing claim that the same mechanism is required for CA Secrets, JWKS validation and the fallback certificate, which this page does not state.

Method: documentation only; no commands were run.
