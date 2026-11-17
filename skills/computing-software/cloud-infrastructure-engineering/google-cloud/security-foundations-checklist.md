---
id: computing-software.cloud-infrastructure-engineering.google-cloud.security-foundations-checklist
name: security-foundations-checklist
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, shared-responsibility, security-foundations-checklist, security-best-practices, enterprise-foundations, security-baseline]
level: practitioner
status: draft
description: "Run a Google Cloud security foundations checklist: identity, hierarchy, network, detective controls, data protection, and the Google security best practices center resources."
sources: ["https://cloud.google.com/architecture/security-foundations", "https://cloud.google.com/security/best-practices", "https://cloud.google.com/docs/enterprise/setup-checklist"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Security foundations checklist

Derived from Google's enterprise foundations blueprint and security best practices center.
Use it to assess an existing organization quickly.

## Identity and access
- [ ] Cloud Identity/Workspace with SSO from the corporate IdP; 2SV enforced (security keys for admins).
- [ ] Super admins: 2-4 dedicated accounts, not used for GCP; break-glass process tested.
- [ ] All IAM via groups; no basic roles at org/folder; no `domain:` grants of project/billing creator.
- [ ] No user-managed SA keys (constraint enforced); WIF for external workloads.
- [ ] Privileged access just-in-time (PAM) for production admin roles.

## Hierarchy and policy
- [ ] Folders by environment/business unit; projects created by a factory with labels and budgets.
- [ ] Baseline org policies enforced (external IP, OS Login, uniform bucket access, DRS, locations).
- [ ] Deny policies protecting critical permissions.

## Network
- [ ] Shared VPC per environment; no default networks; firewall via policies with least privilege.
- [ ] Private Google Access / PSC; Cloud NAT for egress; no public IPs on VMs.
- [ ] VPC Service Controls around sensitive data projects.
- [ ] Cloud Armor in front of public apps.

## Detective controls
- [ ] Org aggregated log sink to a locked central bucket; Data Access logs for sensitive services.
- [ ] Security Command Center active (Premium/Enterprise for threat detection), findings routed.
- [ ] Alerts on IAM changes at org/folder, org policy changes, super admin logins.

## Data protection
- [ ] CMEK where required (Autokey); key admins separated from data admins.
- [ ] Sensitive Data Protection discovery on data warehouses.
- [ ] Backups in vaults with enforced retention.

## Response
- [ ] Essential Contacts set for security/technical/billing.
- [ ] Incident runbooks for leaked keys, compromised accounts, public buckets.

Each unchecked item becomes a remediation ticket with owner and date.
