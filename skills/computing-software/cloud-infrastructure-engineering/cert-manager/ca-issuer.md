---
id: computing-software.cloud-infrastructure-engineering.cert-manager.ca-issuer
name: ca-issuer
category: computing-software
field: cloud-infrastructure-engineering
product: cert-manager
tags: [ca-issuer, tls-crt, intermediate-ca, cluster-resource-namespace, ocspservers, rotation]
level: practitioner
status: docs-checked
description: "Configure a cert-manager CA issuer from a tls.crt/tls.key Secret, handle intermediates, and plan for the missing CA rotation and validation."
sources:
  - https://cert-manager.io/docs/configuration/ca/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Secret requirements: keys named exactly `tls.crt` and `tls.key`, base64-encoded values. It must be in the Issuer's namespace; for a ClusterIssuer it must be in the cluster resource namespace (default `cert-manager`, set by the controller's `--cluster-resource-namespace`). A root can be bootstrapped with a SelfSigned issuer.

Issuer: `spec.ca.secretName` points at the Secret. Optional string arrays `spec.ca.crlDistributionPoints` and `spec.ca.ocspServers` are written into issued certificates. cert-manager does not generate or host CRLs or OCSP responses.

Intermediates: put the full chain in `tls.crt` in order issuer, intermediate(s), root. The root is optional, but including it fills `ca.crt` in issued Secrets. An incomplete chain can stop consumers verifying leaves.

Check: `kubectl get issuers ca-issuer -n <ns> -o wide` should show READY `True` and STATUS "Signing CA verified".

Failure modes and limits:
- No automatic CA rotation; watch CA expiry.
- Leaf certificates can outlive the CA; no duration check.
- Updating the CA Secret does not reissue leaves; run `cmctl renew`.
- CA validity is not checked: it needs basic constraints `isCA: true` and normally the certificate sign key usage. Name constraints and max path length are not validated.
- Output is not publicly trusted; distribute the CA with trust-manager.

## Checked

2026-11-03. Confirmed on the cert-manager CA issuer page (configuration/ca): Secret key names and namespace rules, --cluster-resource-namespace, chain order, CRL and OCSP fields, Signing CA verified status and each item under Important Information. Nothing removed.
Method: documentation only; no commands were run.
