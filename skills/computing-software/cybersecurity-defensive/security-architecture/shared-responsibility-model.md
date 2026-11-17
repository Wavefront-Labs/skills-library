---
id: computing-software.cybersecurity-defensive.security-architecture.shared-responsibility-model
name: shared-responsibility-model
category: computing-software
field: cybersecurity-defensive
product: security-architecture
tags: [security-architecture, shared-responsibility-model, cloud-security, iaas-paas-saas, control-ownership, raci, third-party-risk]
level: practitioner
status: draft
description: "Apply the cloud shared responsibility model: map controls to provider vs customer for IaaS, PaaS and SaaS, build a control ownership matrix and close the gaps in between."
sources: ["https://aws.amazon.com/compliance/shared-responsibility-model/", "https://learn.microsoft.com/en-us/azure/security/fundamentals/shared-responsibility", "https://cloud.google.com/architecture/framework/security/shared-responsibility-shared-fate"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Shared responsibility model

**Goal:** for every cloud service in use, it is written down who operates each security
control, so nothing falls between provider and customer.

## The split by service model
| Layer | IaaS (EC2, Azure VM) | PaaS (RDS, App Service) | SaaS (M365, Salesforce) |
|---|---|---|---|
| Physical, hypervisor, network fabric | Provider | Provider | Provider |
| OS patching and hardening | **Customer** | Provider | Provider |
| Runtime/middleware | **Customer** | Provider (mostly) | Provider |
| Network controls (SGs, firewalls) | **Customer** | Shared (customer configures) | Provider |
| Application code | **Customer** | **Customer** | Provider |
| Identity and access configuration | **Customer** | **Customer** | **Customer** |
| Data classification, encryption choices, backup policy | **Customer** | **Customer** | **Customer** |
| Logging enablement and retention | **Customer** | **Customer** | **Customer** (often licence-dependent) |
The customer always owns identities, data, configuration and who has access. Most cloud
breaches are customer-side misconfiguration, not provider failure.

## Build the control ownership matrix
1. List services in use (from cloud inventories and SaaS discovery).
2. For each, read the provider's responsibility documentation and its SOC 2/ISO reports
   (including **complementary user entity controls**: what the report assumes you do).
3. Map your control framework (CIS, NIST 800-53, ISO 27001 Annex A) to Provider / Customer /
   Shared per service, naming the customer team owning each customer control.
4. Identify gaps: controls nobody owns (e.g. SaaS audit log export, backup of SaaS data,
   key rotation for customer-managed keys).

## Common gaps
- SaaS backups: providers ensure availability, not recovery from your own deletions or
  ransomware in synced data; retention policies or third-party backup needed.
- Logging: default retention short, some logs need premium licences or explicit enablement.
- Managed Kubernetes: provider manages control plane; nodes, workloads, RBAC and network
  policies are yours.
- Serverless: provider patches runtime; function permissions and dependencies are yours.

## Gotchas
- "Shared" without a named customer owner means unowned.
- Provider responsibility changes as services evolve; review annually.
- Google's "shared fate" framing adds provider-supplied secure defaults, but the customer
  still configures and owns access.

## Verify
Pick three services and walk the matrix with their owners; every customer control has an
owner, evidence (config, logs, test results) and no unexplained "shared" entries.
