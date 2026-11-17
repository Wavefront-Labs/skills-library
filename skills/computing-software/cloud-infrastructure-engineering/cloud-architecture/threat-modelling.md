---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.threat-modelling
name: threat-modelling
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, cloud-security-architecture, threat-modelling, stride, data-flow-diagram, trust-boundaries, attack-paths, threat-modeling-tool, threat-dragon]
level: advanced
status: draft
description: "Threat-model a cloud workload: DFD with trust boundaries incl. CI/CD and IAM, STRIDE per element, cloud-specific threats, findings turned into controls and tests."
sources: ["https://owasp.org/www-community/Threat_Modeling_Process", "https://www.threatmodelingmanifesto.org/", "https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/sec_securely_operate_threat_model.html", "https://learn.microsoft.com/azure/security/develop/threat-modeling-tool"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Threat modelling a cloud workload

Four questions (Threat Modeling Manifesto): What are we working on? What can go wrong? What are
we going to do about it? Did we do a good enough job?

## Steps
1. **Diagram** the data flows: users, services, data stores, queues, third parties — and the
   cloud-specific elements people omit: CI/CD pipeline and its credentials, IAM roles and trust
   policies, the provider control plane (console/API), secrets store, logging pipeline, admin access paths.
2. **Mark trust boundaries**: internet ↔ edge, VPC ↔ managed services, account ↔ account,
   workload identity ↔ data, CI ↔ prod.
3. **STRIDE per element/flow**: Spoofing (stolen tokens, forged webhooks), Tampering (unsigned
   artifacts, writable buckets), Repudiation (missing CloudTrail/audit logs), Information
   disclosure (public snapshots, overly broad roles, SSRF to metadata service), Denial of service
   (cost-exhaustion, quota exhaustion), Elevation of privilege (`iam:PassRole`, wildcard policies,
   CI role with admin).
4. **Cloud-specific checklist**: IMDSv1/SSRF, cross-account trust without external ID/conditions,
   public endpoints on managed services, key policy grants, CI OIDC trust scoped to branch/repo,
   log tampering by the same admin.
5. **Rank** (impact × likelihood) and assign mitigations with owners; each mitigation gets a
   verification (policy-as-code rule, test, detective alert).
6. Store the model with the design doc; revisit on significant change.

Tools: OWASP Threat Dragon, Microsoft Threat Modeling Tool, or a whiteboard + table.

## Verify
- [ ] DFD includes CI/CD and admin access paths.
- [ ] Every high-ranked threat has a mitigation and verification.
