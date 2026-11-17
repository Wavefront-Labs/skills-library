---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.compliance-mapping
name: compliance-mapping
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, cloud-security-architecture, compliance-mapping, control-mapping, iso-27001, soc-2, pci-dss, hipaa, csa-ccm, audit-evidence, aws-audit-manager, conformance-packs]
level: advanced
status: draft
description: "Map cloud controls to compliance frameworks (ISO 27001, SOC 2, PCI DSS, HIPAA) via a common control set, inherit provider controls, automate evidence, and keep scope small."
sources: ["https://cloudsecurityalliance.org/research/cloud-controls-matrix", "https://docs.aws.amazon.com/audit-manager/latest/userguide/what-is.html", "https://learn.microsoft.com/azure/governance/policy/samples/", "https://cloud.google.com/security/compliance/offerings"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Mapping cloud controls to compliance frameworks

## Steps
1. **Scope first**: which workloads/accounts handle in-scope data (cardholder data, PHI). Isolate
   them in dedicated accounts/subscriptions — smaller scope, cheaper audits (PCI scope reduction).
2. **Common control framework**: map each framework's requirements onto one internal control set
   (CSA Cloud Controls Matrix maps to ISO 27001/27017/27018, SOC 2, PCI DSS, NIST 800-53 and more).
   Implement once, evidence many times.
3. **Shared responsibility**: provider attestations (AWS Artifact, Microsoft Service Trust Portal,
   Google Compliance Reports Manager) cover physical/infrastructure controls; you document which
   controls are inherited, shared, or yours.
4. **Implement controls as code**: preventive (SCPs/Azure Policy/Org Policy), detective (AWS Config
   conformance packs, Security Hub standards, Azure Policy regulatory compliance initiatives,
   Security Command Center compliance), and procedural (access reviews, change management).
5. **Automate evidence**: AWS Audit Manager frameworks, Azure regulatory compliance dashboard
   exports, scheduled config snapshots, ticket exports. Store with timestamps.
6. Continuous: drift alerts, quarterly access reviews, annual risk assessment.

## Gotchas
- Using a provider "compliance" dashboard score as proof of compliance — it covers only automatable technical checks.
- In-scope data leaking into out-of-scope systems (logs, analytics) expands scope silently.

## Verify
- [ ] Control matrix lists each requirement → control → implementation → evidence source.
- [ ] Evidence for the last quarter retrievable without manual screenshots.
