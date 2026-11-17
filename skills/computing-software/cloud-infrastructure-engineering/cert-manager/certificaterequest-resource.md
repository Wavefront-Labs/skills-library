---
id: computing-software.cloud-infrastructure-engineering.cert-manager.certificaterequest-resource
name: certificaterequest-resource
category: computing-software
field: cloud-infrastructure-engineering
product: cert-manager
tags: [certificaterequest, approved, denied, conditions, signers, approvesignernames, disableautoapproval]
level: advanced
status: docs-checked
description: "Read and reason about cert-manager CertificateRequests: spec, conditions, approval semantics, signer RBAC and the default auto-approver switches."
sources:
  - https://cert-manager.io/docs/usage/certificaterequest/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A CertificateRequest is normally created by the Certificate controller. `spec` is immutable. Fields: `request` (base64 PEM CSR), `isCA`, `usages`, `duration`, `issuerRef` (`name`, `kind` default `Issuer`, `group`). `userInfo` (`username`, `groups`, `uid`, `extra`) is set by cert-manager; requests altering it are rejected.

Conditions:
- `Ready=False` reason `Pending`: issuer missing or issuance underway; reason `Failed`: terminal.
- `Ready=True` reason `Issued`.
- `Approved=True` or `Denied=True`: set only by an approver. They are mutually exclusive and permanent, enforced by the validating webhook. `Denied` is terminal.
- `InvalidRequest=True`: terminal, reason gives the cause.

A signer must not sign without `Approved`, and never signs with `Denied`. Failed issuance is not retried by the request itself.

Default auto-approver covers `cert-manager.io` Issuer and ClusterIssuer. Disable with `disableAutoApproval=true` (v1.15.0+). Extend it to external issuers through `approveSignerNames`; an empty list approves all.

Approver RBAC, at cluster scope: apiGroup `cert-manager.io`, resource `signers`, verb `approve`, with `resourceNames` of the form `<signer-resource-name>.<signer-group>/<signer-namespace>.<signer-name>` (namespaced), `.../<signer-name>` (cluster), or `.../*`.

The page gives a sample manifest and says CertificateRequests are typically managed by controllers or other systems, not humans.

## Checked

2026-11-03. Confirmed on the cert-manager CertificateRequest page (usage/certificaterequest): spec immutability, fields, Ready, Approved, Denied and InvalidRequest conditions, userInfo, approval semantics, auto-approver and disableAutoApproval and approveSignerNames (v1.15.0), RBAC resourceNames syntax. Reworded one sentence about hand-created requests.
Method: documentation only; no commands were run.
