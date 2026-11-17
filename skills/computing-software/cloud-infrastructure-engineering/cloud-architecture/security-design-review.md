---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.security-design-review
name: security-design-review
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, security-foundations, cloud-security-architecture, security-design-review, security-architecture-review, threat-model-review, secure-design-checklist]
level: practitioner
status: docs-checked
description: "Run a security design review for a cloud workload against the Azure Well-Architected security checklist SE:01-SE:12, with ASVS as the application verification reference."
sources: ["https://learn.microsoft.com/azure/well-architected/security/checklist", "https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/welcome.html", "https://owasp.org/www-project-application-security-verification-standard/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Security design review for workloads

## Inputs
Architecture diagrams with trust boundaries, data classification and flows, identity design, network exposure,
third-party components and compliance scope.

## Review checklist (Azure Well-Architected security, SE codes)
- **SE:01 Baseline**: security baseline aligned to compliance requirements, standards and platform recommendations,
  measured regularly.
- **SE:02 SDL**: secure development lifecycle throughout software development.
- **SE:03 Classification**: sensitivity labels on all workload data and systems; use them to shape design.
- **SE:04 Segmentation**: intentional segmentation across networks, roles, workload identities and resources.
- **SE:05 Identity**: strict, conditional, auditable IAM for users, team members and components; least access;
  audit access that is not identity-based.
- **SE:06 Network**: isolate, filter and control ingress and egress, east-west and north-south, in depth.
- **SE:07 Encryption**: modern methods, scope aligned to classification, native platform encryption preferred.
- **SE:08 Hardening**: reduce surface area and tighten configuration of all components.
- **SE:09 Secrets**: harden storage, restrict and audit access, rotate regularly with an emergency path.
- **SE:10 Monitoring**: threat detection integrated with the platform, alerts feeding SecOps processes.
- **SE:11 Testing**: tests that prevent issues, validate preventions and test detection.
- **SE:12 Incident response**: defined and tested procedures, from local issues to disaster recovery, with named owners.

Application controls: OWASP ASVS (current stable release 5.0.0, published 30 May 2025) is a basis for testing
application technical security controls and a requirements list for developers. Cite requirements as
v<version>-<chapter>.<section>.<requirement>, for example v5.0.0-1.2.5.

## Process
1. Scope by data classification and exposure; use a lighter review for low-risk workloads (your own policy).
2. Walk the threat model and check each threat has a control.
3. Record findings with severity, owner and due date; agree locally what blocks go-live.
4. Re-review on significant change.

## Verify
- [ ] Findings tracked with owners; go-live blockers closed or formally accepted.
- [ ] Review artefacts stored with the architecture records.

## Checked
2026-11-08. Confirmed against the Azure Well-Architected security design review checklist (SE:01-SE:12 wording), the
OWASP ASVS project page (purpose, 5.0.0 published 30 May 2025, identifier format) and the AWS Security Pillar
introduction (scope only; it gives no checklist). Removed: ASVS levels, specific DDoS, WAF, MFA and supply-chain items
and the critical/high/medium/low scheme, none of which those pages state. Tiering and severity gating are marked as
local policy.
Method: documentation only; no commands were run.
