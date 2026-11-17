---
id: computing-software.cybersecurity-defensive.cloud-security.cspm-auto-remediation
name: cspm-auto-remediation
category: computing-software
field: cybersecurity-defensive
product: cloud-security
tags: [cspm-auto-remediation, auto-remediation, security-hub-automation, eventbridge, azure-policy-remediation, guardrails, cspm]
level: advanced
status: draft
description: "Auto-remediate cloud posture findings safely: which findings to auto-fix, EventBridge/Lambda and SSM, Azure Policy modify/DINE, preventive guardrails first, and change safety."
sources: ["https://docs.aws.amazon.com/securityhub/latest/userguide/securityhub-cloudwatch-events.html", "https://aws.amazon.com/solutions/implementations/automated-security-response-on-aws/", "https://learn.microsoft.com/en-us/azure/governance/policy/how-to/remediate-resources", "https://cloud.google.com/security-command-center/docs/how-to-configure-security-command-center"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Auto-remediation of posture findings

## Prefer prevention
Each auto-remediation exists because something was allowed to be created wrong. First add preventive
guardrails (SCPs/RCPs, Azure Policy deny, GCP org policies, IaC scanning) so the finding cannot recur;
remediation then handles drift and legacy.

## What to auto-fix (low blast radius, high confidence)
- S3 Block Public Access on accounts/buckets not tagged as public sites.
- Enable default encryption, versioning, logging.
- Remove `0.0.0.0/0` on SSH/RDP security group rules.
- Disable unused IAM access keys > 90 days (notify first).
- Turn on GuardDuty/Config/CloudTrail where disabled.
**Not** auto-fixed: anything that can cause outages (deleting resources, changing routing, IAM policy rewrites) - ticket to owner instead.

## AWS pattern
Security Hub finding (ASFF) -> EventBridge rule (filter on `ProductFields.ControlId` and `Workflow.Status=NEW`) -> Lambda or SSM Automation runbook -> update finding workflow status and note. AWS's "Automated Security Response on AWS" solution provides runbooks for Security Hub controls, deployable across the org.

## Azure
Azure Policy `Modify` and `DeployIfNotExists` effects with remediation tasks (managed identity with minimal
roles); Defender for Cloud workflow automation (Logic Apps) for notifications.

## GCP
SCC findings -> Pub/Sub notifications -> Cloud Functions/Run to remediate.

## Safety
- Exemption tags (`security-exception=SEC-123`) honoured by the remediation code, with expiry.
- Dry-run/notify-only phase per rule; rate limits; full audit log of every action with before/after.
- Owner notification after each fix.

## Verify
- [ ] Test resource created non-compliant is fixed within the SLA and owner notified.
- [ ] Exempted resource left untouched.
