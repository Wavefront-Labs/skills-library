---
id: computing-software.cloud-infrastructure-engineering.cert-manager.annotations-reference
name: annotations-reference
category: computing-software
field: cloud-infrastructure-engineering
product: cert-manager
tags: [annotations, reference, ingress-shim, certificaterequest, inject-ca-from, temporary-certificate]
level: practitioner
status: docs-checked
description: "Map cert-manager annotation keys to the resource they belong on and the Certificate spec field they set, across Ingress, Gateway, Certificate, requests and injectables."
sources:
  - https://cert-manager.io/docs/reference/annotations/
  - https://cert-manager.io/docs/usage/ingress/
  - https://cert-manager.io/docs/usage/gateway/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
On Ingress and Gateway (tune generated Certificates): `cert-manager.io/issuer`, `cluster-issuer`, `issuer-kind`, `issuer-group`; `common-name`, `duration`, `renew-before`, `renew-before-percentage`, `revision-history-limit` (minimum 1), `secret-template`, `email-sans`, `ip-sans`, `uri-sans`, `usages` (comma-separated), `subject-*` (countries, localities, organizationalunits, organizations, postalcodes, provinces, serialnumber, streetaddresses), and `private-key-algorithm` (`RSA` default), `private-key-encoding` (`PKCS1` default), `private-key-size` (RSA 2048 default, ECDSA 256), `private-key-rotation-policy`. Note the pages disagree on the rotation default: the annotations page says `Never`, the Ingress and Gateway pages say `Always`; set it explicitly.

Ingress only: `acme.cert-manager.io/http01-edit-in-place` (`"true"` edits the existing Ingress and adds the temporary-certificate annotation), `http01-ingress-class`, `http01-ingress-ingressclassname`; `kubernetes.io/tls-acme` needs a default issuer; `kubernetes.io/ingress.class` is deprecated. `venafi.cert-manager.io/custom-fields` (Certificate, Ingress or Gateway) passes JSON custom fields to the CyberArk issuer.

On Certificates: `cert-manager.io/alt-names` (sets `spec.dnsNames`), `issue-temporary-certificate`, and auto-added `acme.cert-manager.io/http01-parentrefkind` and `-parentrefname` when created from a Gateway or ListenerSet.

On CertificateRequests: `cert-manager.io/certificate-name`, `certificate-revision`, `private-key-secret-name`, `venafi.cert-manager.io/pickup-id`, and the experimental `experimental.cert-manager.io/request-duration`, `request-is-ca` and `private-key-secret-name` (the last used by the self-signing issuer).

CA injection: `cert-manager.io/inject-ca-from`, `inject-ca-from-secret`, `inject-apiserver-ca` on CRDs, webhook configurations and APIServices; `cert-manager.io/allow-direct-injection` on the source Secret. The page does not say who sets the request, Secret and injection annotations.

## Checked

2026-11-03: Confirmed against the Annotations page: the Ingress/Gateway annotations and the Certificate spec fields they set, `revision-history-limit` minimum 1, algorithm/encoding/size defaults and valid values, the Ingress-only HTTP01 annotations, `kubernetes.io/tls-acme` and `ingress.class` notes, Certificate annotations, CertificateRequest annotations, injection annotations and `allow-direct-injection`. The `private-key-rotation-policy` default conflict is real: the Annotations page says `Never` while the Ingress and Gateway usage pages say `Always`; both pages were read and added to sources. Fixed: `venafi.cert-manager.io/custom-fields` applies to Certificate, Ingress and Gateway (not Ingress only), and the CertificateRequest annotation list now distinguishes `cert-manager.io/private-key-secret-name` from the experimental one.

Method: documentation only; no commands were run.
