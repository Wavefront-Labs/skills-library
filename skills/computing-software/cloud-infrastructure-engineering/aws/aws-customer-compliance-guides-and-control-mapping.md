---
id: computing-software.cloud-infrastructure-engineering.aws.aws-customer-compliance-guides-and-control-mapping
name: aws-customer-compliance-guides-and-control-mapping
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, shared-responsibility, compliance-guides, customer-compliance-guides, aws-artifact, audit-manager, control-mapping]
level: practitioner
status: draft
description: "Map AWS services to compliance: AWS Artifact reports, Customer Compliance Guides per service, Services in Scope, and evidence via Audit Manager, Config and Security Hub."
sources: ["AWS Compliance - Customer Compliance Guides", "AWS Artifact User Guide - Downloading reports and managing agreements", "AWS Services in Scope by Compliance Program", "AWS Audit Manager User Guide - Frameworks and evidence"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Customer compliance guides and control mapping

**Goal:** for an audit (SOC 2, ISO 27001, PCI DSS, HIPAA, NIST 800-53, regional frameworks), show which
controls AWS provides, which are shared, and how you meet your part, with evidence.

## Sources
| Source | Use |
|---|---|
| **AWS Artifact** | download AWS's own audit reports (SOC 1/2/3, ISO certificates, PCI AoC, C5, etc.) and accept agreements (e.g. HIPAA BAA) |
| **Services in Scope** page | confirm each service you use is in scope for the program |
| **Customer Compliance Guides (CCGs)** | per service, map security configuration options to framework controls and explain customer responsibilities |
| Security Hub standards | automated checks for AWS FSBP, CIS, PCI DSS, NIST 800-53 |
| Config conformance packs ("Operational Best Practices for X") | rule sets mapped to frameworks |
| Audit Manager frameworks | collect evidence continuously against prebuilt or custom frameworks |

## Building the control matrix
1. List framework controls (e.g. ISO 27001 Annex A or SOC 2 TSC).
2. For each control classify: **inherited** (physical security, hardware disposal: cite the AWS report section),
   **shared** (patching, configuration, awareness: AWS does its layer, you do yours), or **customer-specific** (your data, IAM, application logic).
3. For shared and customer controls, cite the CCG guidance for each service and the implementation (SCP, Config rule, runbook).
4. Attach evidence sources: Audit Manager assessments, Config compliance history, Security Hub findings, CloudTrail, tickets.

## Practical steps
```bash
aws auditmanager list-assessment-frameworks --framework-type Standard \
  --query 'frameworkMetadataList[].[name,id]' --output table
```
- Create an assessment for the framework, scope accounts and services, assign control owners, delegate evidence review.
- Keep Artifact reports current in the audit pack (they are periodic; download the latest for each audit window and respect their NDA terms).

## Gotchas
- A service being "in scope" does not make your use compliant; configuration and process are yours.
- Audit Manager evidence is supporting material, not a certification.
- Regions and partitions differ in program coverage (GovCloud, China, sovereign regions).

## Verify
- [ ] Control matrix lists inherited/shared/customer per control with evidence links.
- [ ] Every service in use checked against Services in Scope for each program.
