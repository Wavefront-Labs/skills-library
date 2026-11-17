---
id: computing-software.cloud-infrastructure-engineering.aws.shared-responsibility-model
name: shared-responsibility-model
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, shared-responsibility, security-of-the-cloud, security-in-the-cloud, compliance, aws-artifact, soc2, iso27001, pci-dss, hipaa, managed-services-responsibility, patching-responsibility, encryption-responsibility, inherited-controls, shared-controls, customer-controls, audit-evidence, security-of-vs-in-the-cloud, inherited-control-mapping]
level: practitioner
status: draft
description: "Apply the AWS shared responsibility model precisely: what AWS secures per service type (EC2, RDS, Lambda, S3), what stays yours (patching, IAM, encryption, data, backups), and audit evidence."
sources: ["AWS Security Documentation - Shared Responsibility Model", "AWS Artifact User Guide - Downloading reports and agreements", "AWS Compliance - Customer Compliance Guides and Services in Scope", "AWS Well-Architected Framework - Security Pillar"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Shared responsibility model — knowing exactly which half of security is yours

**Goal:** for every service you run, you can say what AWS guarantees (and prove it with
their audit reports) and what your team must do — and that list is turned into owned
controls rather than assumed to be "handled by the cloud".

## 1. The split
- **AWS: security *of* the cloud** — physical data centres, hardware, hypervisor, host OS,
  network backbone, the managed service software (RDS engine patching, Lambda runtime
  hosts, S3 durability), and global/regional control-plane availability.
- **You: security *in* the cloud** — your data (classification, encryption choices, backup),
  identity and access (IAM, SSO, keys), OS/network/firewall configuration on what you
  manage, application code, client-side encryption and TLS configuration, logging and monitoring, compliance of your usage.
- **Shared controls**: patch management (AWS patches infrastructure; you patch guest OS/apps),
  configuration management (AWS configures infrastructure; you configure services),
  awareness/training (both sides' staff).
- Compliance frameworks map the same way: AWS holds SOC/ISO/PCI for *their* scope;
  your attestation covers your configuration and data handling.

## 2. By service type (where it moves)
| Service | AWS does | You still do |
|---|---|---|
| **EC2** | Hardware, hypervisor, physical network | Guest OS patching, hardening, agents, SG/NACL, IAM instance role, EBS encryption on, backups, app security |
| **RDS / ElastiCache / MSK** | Engine install, OS patching, host failover, backups mechanism | Choose Multi-AZ, enable encryption/KMS, set maintenance window, DB users/roles, parameter groups, network exposure, backup retention, test restores |
| **ECS/EKS on EC2** | Control plane (EKS), orchestration | Node AMI/patching, pod security, image scanning, IAM/RBAC, network policy |
| **Fargate / Lambda** | Host OS, runtime patching, isolation | Code, dependencies (your `requirements.txt` CVEs), IAM role, env var secrets, timeouts/concurrency, VPC config |
| **S3 / DynamoDB** | Durability, infrastructure, SSE-S3 keys | Bucket/table policies, Block Public Access, encryption key choice, versioning/backup, object lock, access logging, lifecycle |
| **Managed services (SaaS-like: QuickSight, Connect)** | Almost everything underneath | Users, permissions, data classification, integrations |
Rule: the more managed the service, the more responsibility shifts to AWS — but **identity,
data and configuration never move**.

## 3. Turn it into owned controls
1. Inventory services in use (Config aggregator / Cost Explorer by service).
2. For each, write the customer-side controls as a checklist with an owner and evidence
   source (e.g. "EC2 guest patching — Patch Manager compliance report, owner: platform").
3. Map to your framework (ISO 27001 Annex A, SOC 2 criteria, PCI DSS requirements) using
   the **AWS Customer Compliance Guides** (per-service guidance on which requirements you must address).
4. Enforce with code: Security Hub standards (FSBP, CIS), Config conformance packs, SCPs — these implement *your* half.
5. Review when adopting a new service: `Services in Scope` page confirms it is covered by the
   AWS attestations you rely on (PCI, HIPAA eligibility, FedRAMP); if not, you own more or cannot use it for that data.

## 4. Evidence for auditors
- **AWS Artifact** → *Reports*: download SOC 1/2/3, ISO 27001/27017/27018/27701, PCI DSS AOC,
  C5, IRAP, etc. (NDA click-through); *Agreements*: BAA (HIPAA), GDPR DPA addendum (now part of the service terms), accept at org level.
- Give auditors: the SOC 2 Type II for AWS's half + your own evidence (Security Hub scores,
  Config compliance, CloudTrail, Patch Manager, IAM Access Analyzer, backup reports) for yours.
- **Audit Manager** automates evidence collection against frameworks (SOC 2, PCI, GDPR,
  CIS) from your accounts; combine with Artifact for the AWS side.
- AWS **does not** access or back up your data on your behalf, does not manage your IAM, and cannot be a controller for your personal data processing — document that in your DPIA.

## 5. Common misreadings
- "RDS is managed so backups are handled" — the *mechanism* is; retention, cross-region copies, restore testing and deletion protection are yours.
- "Lambda has no OS to patch" — your dependencies and runtime version are yours; deprecated runtimes stop receiving patches.
- "S3 is encrypted by default" — SSE-S3 is on by default, but key management, bucket policies and public access are yours; default encryption does not satisfy "customer-managed keys" requirements.
- "AWS is PCI compliant so we are" — only AWS's infrastructure scope; your cardholder data environment still needs your assessment.
- "AWS monitors for intrusions" — on their infrastructure; GuardDuty/Detective for your accounts must be enabled by you.
- "Multi-AZ is automatic" — it is an option you select and pay for.

## Gotchas
- Shared *controls* need two owners; "AWS does it" is not an owner on your side.
- Managed service maintenance windows are AWS-initiated; you own the impact — set windows and test failover.
- Marketplace/third-party AMIs and SaaS have their own responsibility splits; read their models.
- Regional opt-in and data residency are your configuration choices, not AWS defaults.
- Unconfirmed: exact current names of Artifact agreements and the Customer Compliance Guide catalogue — check Artifact.

## Verify
- [ ] A one-page matrix exists listing each service in use, AWS vs customer controls, owner and evidence source.
- [ ] Artifact reports for the frameworks you claim are downloaded and dated within 12 months.
- [ ] Every "customer" control maps to an enforced check (Security Hub control id, Config rule, SCP) or a documented manual procedure.
- [ ] New-service adoption checklist includes a Services-in-Scope lookup.
- [ ] Last audit's findings did not include an item that was assumed to be "AWS's responsibility".
