---
id: computing-software.cloud-infrastructure-engineering.cert-manager.csi-driver-spiffe
name: csi-driver-spiffe
category: computing-software
field: cloud-infrastructure-engineering
product: cert-manager
tags: [csi-driver-spiffe, spiffe, trust-domain, svid, approver, fs-group]
level: advanced
status: docs-checked
description: "Issue SPIFFE identities to pods with csi-driver-spiffe: volume attributes, ID format, trust domain, built-in approver rules and the issuer ConfigMap failure modes."
sources:
  - https://cert-manager.io/docs/usage/csi-driver-spiffe/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Driver `spiffe.csi.cert-manager.io`, mounted `readOnly: true`. Attribute `spiffe.csi.cert-manager.io/fs-group` sets the volume group (e.g. `"456"`); without it a Pod that specifies a user or group cannot read the volume.

SPIFFE ID, carried as a URI SAN: `spiffe://<trust-domain>/ns/<namespace>/sa/<serviceaccount>`. Trust domain is set at install with Helm `app.trustDomain`; requests with another domain are rejected by the approver.

Approver: a separate approver Deployment must approve requests, only for CertificateRequests with annotation `spiffe.csi.cert-manager.io/identity`. It enforces: usages limited to Key Encipherment, Digital Signature, Client Auth, Server Auth; duration equal to the enforced duration (default 1 hour); no SANs except one URI SAN, which must be the creating ServiceAccount's SPIFFE ID.

Issuer selection: ConfigMap named by `app.runtimeIssuanceConfigMap` with keys `issuer-name`, `issuer-kind`, `issuer-group`. If it is deleted or invalid it is ignored and the install-time default issuer is used; with neither, issuance and Pod creation fail.

Security: the driver uses the Pod's token, so each ServiceAccount that mounts the volume needs permission to create CertificateRequests. A compromised Pod with that right could request from any issuer in the cluster, so other approvers (approver-policy) must not overlap and must restrict issuers. For the CA bundle prefer trust-manager over the static root option.

## Checked

2026-11-03: Confirmed against the csi-driver-spiffe page: driver `spiffe.csi.cert-manager.io`, `readOnly: true`, `fs-group` attribute and its purpose, SPIFFE ID shape from the examples (`spiffe://<trust domain>/ns/<namespace>/sa/<serviceaccount>`), the separate approver and its five checks (usages, 1 hour default duration, single URI SAN, trust domain), the `spiffe.csi.cert-manager.io/identity` annotation, runtime issuer ConfigMap keys and `app.runtimeIssuanceConfigMap`, fallback and failure behaviour, the security notes on CertificateRequest permission and overlapping approvers, and the trust-manager recommendation over the static root bundle. Nothing removed.

Method: documentation only; no commands were run.
