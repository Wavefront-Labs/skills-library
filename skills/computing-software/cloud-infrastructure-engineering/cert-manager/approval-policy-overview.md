---
id: computing-software.cloud-infrastructure-engineering.cert-manager.approval-policy-overview
name: approval-policy-overview
category: computing-software
field: cloud-infrastructure-engineering
product: cert-manager
tags: [approval, auto-approval, csr, approval-condition, policy]
level: intro
status: docs-checked
description: "Understand where cert-manager rejects requests (before and after the issuer), why default auto-approval is not for production, and where to look next."
sources:
  - https://cert-manager.io/docs/policy/approval/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Requests can be rejected at two points in issuance:
1. Before the CSR reaches the issuer: cert-manager itself refuses non-conforming requests.
2. After the issuer receives it: the issuer decides what to reject and what error to return.

Pre-issuer approval: cert-manager requires a CertificateRequest to be approved before sending it to the issuer, and Kubernetes CertificateSigningRequests must also be approved. Approval is an "approval condition" added to the resource.

Default behaviour: a default install automatically approves every CertificateRequest and CertificateSigningRequest that uses cert-manager's built-in issuers. This eases first use and is not recommended for production. Instead run a stricter auto-approver that limits who can request which certificates; approver-policy is the named example.

After the CSR, an issuer may accept everything and overwrite non-conforming CSR properties, or map CSR properties to certificate properties by any logic (see issuing policy).

The page does not cover RBAC verbs, condition fields or approver-policy configuration.

## Checked

2026-11-03: Confirmed against the Approval Policy page: the two rejection points, approval being required before the issuer, default auto-approval of built-in issuer requests, the production warning, approver-policy as the example, and issuer autonomy after the CSR. Removed: the pointer to the CertificateRequest page for `Approved`/`Denied` conditions (not on this page).

Method: documentation only; no commands were run.
