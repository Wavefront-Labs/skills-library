---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.shared-responsibility-model
name: shared-responsibility-model
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, service-models, shared-responsibility-model, responsibility-matrix, security-of-the-cloud, security-in-the-cloud, raci, customer-responsibility]
level: practitioner
status: docs-checked
description: "Turn the shared responsibility model into a per-service responsibility matrix: what the provider covers, what you configure, and which team owns each part."
sources: ["https://aws.amazon.com/compliance/shared-responsibility-model/", "https://learn.microsoft.com/azure/security/fundamentals/shared-responsibility", "https://cloud.google.com/architecture/framework/security/shared-responsibility-shared-fate"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Shared responsibility model by service

AWS frames it as security "of" the cloud (the provider protects the hardware, software, networking and facilities) versus
security "in" the cloud (customer responsibility depends on the services chosen). Customer responsibility also varies
with the Regions, how services are integrated, and applicable laws and regulations.

## Matrix (Microsoft Azure's illustrative table)
| Area | On-prem | IaaS | PaaS | SaaS |
|---|---|---|---|---|
| Customer data | Customer | Customer | Customer | Customer |
| Configurations and settings | Customer | Customer | Customer | Customer |
| Identities and users | Customer | Customer | Customer | Customer |
| Client devices | Customer | Customer | Customer | Shared |
| Applications | Customer | Customer | Shared | Shared |
| Network controls | Customer | Customer | Shared | Microsoft |
| Operating system | Customer | Customer | Microsoft | Microsoft |
| Physical hosts, network, datacenter | Customer | Microsoft | Microsoft | Microsoft |

Always retained by the customer (Azure): data (classification, protection, encryption decisions), endpoints, accounts
and access management (RBAC, MFA, conditional access). Microsoft states the table is governance guidance, not a legal
conclusion, and does not modify any agreement.

## Provider-specific notes
- **AWS**: for EC2 (IaaS) the customer manages the guest OS including patches, installed software and the security
  group. For abstracted services such as S3 and DynamoDB, AWS runs the infrastructure, OS and platform; the customer
  manages data (including encryption options), asset classification and IAM permissions. Controls are inherited
  (physical and environmental), shared (patch management, configuration management, awareness and training) or
  customer-only (for example zone security).
- **Google Cloud**: IaaS (Compute Engine, Cloud Storage, networking) leaves the bulk of security with you; in PaaS
  (App Engine, GKE, BigQuery) you share application-level controls and IAM and remain responsible for data security;
  in SaaS (Workspace) Google owns most, you keep access controls and data; FaaS is similar to SaaS. The provider always
  owns underlying network and infrastructure, and you always own access policies and data.

## Steps
1. For each service in use, read the provider's security documentation for that service and list customer-configurable
   controls (AWS suggests the security chapters of each service's documentation).
2. Build the matrix per service and assign an internal owner (platform, application or security team).
3. Consider regulatory frameworks (PCI DSS, HIPAA, GDPR data location): inherited controls can be evidence for
   auditors; check the provider's compliance resources.
4. Use provider attestation reports to determine inherited controls and what remains.
5. Revisit when services or regulations change. Google calls its extension "shared fate": secured blueprints and
   landing zones with recommendations enabled by default, to reduce misconfiguration, which it says is the root cause of
   most breaches.

## Gotchas
- Workloads often mix IaaS, PaaS, SaaS; check how controls interact and overlap across them.
- Key management and incident management are areas where responsibilities are not easily defined (Google).

## Verify
- [ ] Matrix covers every service in use, with owners.

## Checked
Method: docs-only read of cited pages, 2026-11-08

Confirmed against the AWS Shared Responsibility Model page, Azure shared responsibility article and Google Cloud shared
responsibility and shared fate page. Removed: the invented FaaS column, per-layer P/C cells that differ from the
Azure table (OS patching, runtime, network in SaaS), and the CSPM monitoring step, which the pages do not cover.
