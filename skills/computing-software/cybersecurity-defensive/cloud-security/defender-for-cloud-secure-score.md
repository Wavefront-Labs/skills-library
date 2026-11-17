---
id: computing-software.cybersecurity-defensive.cloud-security.defender-for-cloud-secure-score
name: defender-for-cloud-secure-score
category: computing-software
field: cybersecurity-defensive
product: cloud-security
tags: [cspm, secure-score, microsoft-defender-for-cloud, security-recommendations, governance-rules, azure-policy-initiative]
level: practitioner
status: docs-checked
description: "Raise Microsoft Defender for Cloud secure score meaningfully: control weighting, prioritising recommendations, exemption types, governance rules and trend tracking."
sources: ["https://learn.microsoft.com/en-us/azure/defender-for-cloud/secure-score-security-controls", "https://learn.microsoft.com/en-us/azure/defender-for-cloud/governance-rules", "https://learn.microsoft.com/en-us/azure/defender-for-cloud/exempt-resource"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Defender for Cloud secure score

**Goal:** use secure score as a prioritised remediation driver for Azure (and connected AWS/GCP) posture, not a vanity number.

## How it is calculated
- Only built-in recommendations from the Microsoft cloud security benchmark (MCSB) affect the secure score. Recommendations are grouped into security controls (for example Enable MFA, Secure management ports, Apply system updates, Remediate vulnerabilities, Encrypt data in transit).
- Each control has a fixed **max score** that shows its relative significance. A control's current score is its max score divided by the number of healthy plus unhealthy resources, multiplied by the number of healthy resources. To earn all of a control's points, every resource must comply with every recommendation in that control.
- Preview recommendations do not count until they are generally available.
- Across several subscriptions or connectors the score is a weighted sum, not a simple average, and a subscription with no assessments for a control is left out of that control.
- Docs state that risk prioritisation does not currently affect the classic secure score. A separate **Cloud secure score (risk-based)** weighs open recommendations by risk level, asset risk factors (such as internet exposure and data sensitivity) and asset criticality.

## Prioritise
1. Use the **Max score** and **Potential score increase** columns (remaining points in a control) to decide what to fix first.
2. High-weight controls on the docs page include Enable MFA, Secure management ports (just-in-time VM access and network security groups), Apply system updates and Remediate vulnerabilities.
3. Where the risk-based score is available, focus on recommendations with higher risk levels, as they contribute most to it.

## Remediate at scale
- Use **Fix** where offered. **Enforce** deploys a policy that remediates new noncompliant resources, and **Deny** blocks creation of noncompliant resources.
- Fix in IaC, not the portal, to avoid drift.
- **Governance rules** auto-assign an owner and due date to recommendations, matched by severity, risk level or recommendation category. The owner can be set by resource tag key or by email address. Due dates are 7, 14, 30 or 90 days after the rule triggers. An optional **grace period** keeps MCSB recommendations from affecting the score until they are overdue. By default owners and their managers get weekly email about open and overdue tasks. Rules need Contributor, Security Admin or Owner on the subscription.

## Exemptions
Exempt with a justification and an optional expiration date instead of disabling a recommendation. The two types affect score differently:
- **Mitigated** (resolved through a third-party service): the resource counts as healthy, so the score rises.
- **Risk accepted (waiver)**: the resource is excluded from the score calculation.
Exemptions can be applied to a resource, subscription or management group. Preview recommendations have no score impact whatever the exemption status. Review exemptions regularly so accepted risk is reassessed.

## Track
The workbooks page includes a ready-made Secure Score Over Time report for subscriptions and controls. Report the trend monthly per subscription owner.

## Gotchas
- The score moves when new resources or new recommendations appear. Explain this to leadership.
- Chasing points by exempting rather than fixing. A Mitigated exemption raises the score without any remediation by you.

## Verify
- [ ] Governance rules assign every high-severity recommendation an owner and due date.
- [ ] Exemptions have expiry dates and justification.
- [ ] Monthly secure score trend reported by subscription.

## Checked
Checked 2026-11-09 against the three Microsoft Learn pages in `sources` (score equation and max score, preview handling, risk-based score note, governance rule options and defaults, exemption types and score effect, workbook report). Removed unconfirmed claims: Azure Policy DeployIfNotExists/Modify effects, the Resource Graph exemption query, continuous export to Log Analytics, attack path analysis and cloud security explorer, and specific quick-win items not on the pages (endpoint protection, storage settings).
Method: documentation only; no commands were run.
