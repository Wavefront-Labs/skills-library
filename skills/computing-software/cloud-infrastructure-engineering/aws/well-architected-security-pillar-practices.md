---
id: computing-software.cloud-infrastructure-engineering.aws.well-architected-security-pillar-practices
name: well-architected-security-pillar-practices
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, well-architected, security-pillar-practices, security-pillar, incident-response, data-protection, identity-foundations]
level: practitioner
status: docs-checked
description: "Well-Architected Security pillar as concrete controls: identity, detection, infrastructure and data protection, incident response and application security, with evidence."
sources: ["https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/welcome.html", "https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/sec_securely_operate_aws_account.html", "https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/sec_permissions_least_privileges.html", "https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/sec_protect_data_transit_encrypt.html", "https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/sec_protect_compute_hardened_images.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Well-Architected Security pillar practices

The pillar has 11 questions (SEC 1 to SEC 11) with numbered best practices (for example `SEC01-BP01`). Use this as a
checklist when answering the questions; each line is a practice and the evidence a reviewer should ask for.

## Security foundations (SEC 1)
- [ ] SEC01-BP01: workloads separated using accounts (AWS Organizations, landing zone).
- [ ] SEC01-BP02: root user secured: MFA always on, no root access keys (remove any that exist and use IAM role
      temporary credentials instead).
- [ ] SEC01-BP07: threat model for the workload, reviewed on major change.

## Identity and access (SEC 2-3)
- [ ] SEC02-BP01/BP02: strong sign-in mechanisms and temporary credentials; SEC02-BP04 a centralised identity provider.
- [ ] SEC02-BP03: secrets stored and used securely; SEC02-BP05 credentials audited and rotated.
- [ ] SEC03-BP02: least privilege; IAM Access Analyzer finds external and unused access and its policy generation
      helps tighten policies; permissions boundaries are an option for delegated administration.
- [ ] SEC03-BP03: emergency access (break-glass) process, tested; SEC03-BP05 organisation permission guardrails.

## Detection (SEC 4)
- [ ] SEC04-BP01/BP02: service and application logging captured in standardised locations.
- [ ] SEC04-BP03/BP04: alerts correlated and enriched; remediation initiated for non-compliant resources.

## Infrastructure protection (SEC 5-6)
- [ ] SEC05-BP01..BP04: network layers, controlled traffic flow within layers, inspection-based protection,
      automated network protection.
- [ ] SEC06-BP01..BP05: vulnerability management, compute from hardened images (EC2 Image Builder can automate
      hardening recipes), less manual and interactive access, software integrity validation, automated protection.

## Data protection (SEC 7-9)
- [ ] SEC07: data classification scheme, controls by sensitivity, automated classification, lifecycle management.
- [ ] SEC08: secure key management, encryption at rest enforced and automated, access control.
- [ ] SEC09-BP01..BP03: key and certificate management, encryption in transit enforced (guidance includes requiring
      at least TLS 1.2 for clients calling AWS APIs; avoid deprecated SSL/TLS versions and self-signed certificates),
      authenticated network communications.

## Incident response (SEC 10)
- [ ] SEC10-BP01..BP08: key personnel identified, incident management plans, forensic capabilities, tested
      playbooks, pre-provisioned access and pre-deployed tools, simulations (game days), learning framework.

## Application security (SEC 11)
- [ ] SEC11-BP01..BP08: security training, automated testing across the lifecycle, regular penetration testing, code reviews, centralised package and dependency services,
      programmatic deployment, pipeline security assessment, security ownership in workload teams.

## Review tips
"In place" means operating with evidence (reports, tickets, configuration). Typical high-risk findings: old IAM user
access keys, logging gaps in some accounts or Regions, no incident playbooks, unencrypted legacy data stores.

## Verify
- [ ] Security pillar answered with evidence links; high-risk issues have owners and dates.

## Checked
Date: 2026-10-27. Documentation release: AWS Well-Architected Security pillar (latest). Confirmed: question and
best-practice numbering and titles SEC01-BP01 to SEC11-BP08 against the pillar contents page, root user MFA and
access-key guidance (SEC01-BP02), Access Analyzer, policy generation and permissions boundary mentions
(SEC03-BP02), EC2 Image Builder for hardening (SEC06-BP02) and the at-least-TLS-1.2 guidance (SEC09-BP02). Removed
specifics no page confirmed: centralised root access, IRSA/Pod Identity, IMDSv2, Inspector, Session Manager,
S3 Block Public Access, Vault Lock, and named product lists for detection. Replaced prose-title `sources`.
Method: documentation only; no commands were run.
