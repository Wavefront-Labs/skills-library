---
id: computing-software.cloud-infrastructure-engineering.cert-manager.threat-model
name: threat-model
category: computing-software
field: cloud-infrastructure-engineering
product: cert-manager
tags: [threat-model, rbac, multi-tenant, clusterissuer, ssrf, secret-exfiltration]
level: sme
status: docs-checked
description: "Apply cert-manager's threat model: which RBAC to restrict, why Issuer and ClusterIssuer edit rights equal secret read, and multi-tenant guidance."
sources:
  - https://cert-manager.io/docs/devops-tips/threat-modelling/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Assets: X.509 private keys and certificates in Secrets; credentials such as Vault tokens read from Secrets; cert-manager's cluster-wide Secret create, read and update permissions.

RBAC guidance:
- `Certificate`, `CertificateRequest`, `Issuer`, `ClusterIssuer`: create, edit and delete are highly privileged; restrict as far as possible and minimise view. Manage them as infrastructure by humans or automation, not by running code.
- `Order` and `Challenge`: only cert-manager should create or edit them; minimise view.

Threats:
- Creating or editing an `Issuer` is effectively reading that namespace's Secrets: an attacker can send secret values to a server they control.
- Creating or editing a `ClusterIssuer` exposes Secrets in cert-manager's install namespace.
- SSRF via ACME: an ACME Issuer with a custom server URL makes cert-manager issue in-cluster requests and return the responses.
- Challenge solver configuration can also send Secret values to attacker endpoints.
- Confused deputy: cert-manager's privileges can be driven through custom resources.
- Identity forgery: broad `Certificate` creation lets attackers impersonate users or services.

Mitigations: tightly scoped RBAC is the primary control; egress restrictions only partly help; enforce approval policies.

Multi-tenant clusters: keep permissions namespace-scoped, treat `ClusterIssuer` as hazardous and deploy it only with a threat model and strict approval policies, provide cert-manager resources to tenants as standard infrastructure, and do not share CA certificates between tenants.

## Checked

2026-11-03: Confirmed against the Threat Model page: the assets and cluster-wide Secret permissions, RBAC guidance for Certificate, CertificateRequest, Issuer, ClusterIssuer, Order and Challenge, the Issuer-equals-secret-read, ClusterIssuer, ACME SSRF and Challenge risks, confused deputy and identity forgery, egress restriction as a partial mitigation, and the four multi-tenant recommendations. Nothing removed.

Method: documentation only; no commands were run.
