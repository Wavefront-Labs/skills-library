---
id: computing-software.cloud-infrastructure-engineering.azure.secure-score-and-recommendation-remediation
name: secure-score-and-recommendation-remediation
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, defender-for-cloud, secure-score, security-recommendations, secure-score-remediation, quick-fix, mcsb]
level: practitioner
status: docs-checked
description: "Raise Defender for Cloud secure score: prioritise recommendations by risk and score impact, use Fix/quick fix and policy remediation, exempt correctly, and track trend with ARG."
sources: ["https://learn.microsoft.com/azure/defender-for-cloud/secure-score-security-controls", "https://learn.microsoft.com/azure/defender-for-cloud/implement-security-recommendations", "https://learn.microsoft.com/azure/defender-for-cloud/exempt-resource", "https://learn.microsoft.com/azure/defender-for-cloud/review-security-recommendations"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Secure score and recommendation remediation

**Goal:** a repeatable weekly loop that fixes the highest-risk findings first and makes the
score move for real reasons.

## How the score works
Recommendations (from the Microsoft Cloud Security Benchmark initiative) roll up into
**security controls** with max points; see the secure score page for how control points are earned.
With Defender CSPM, recommendations are also **risk-prioritised** (risk level by attack paths,
internet exposure, sensitive data).

## Prioritise
1. Defender for Cloud → Recommendations → group by *Risk level* (CSPM) or by control "potential score increase".
2. Export the recommendation list for owners.

## Remediate
- **Fix** button (quick fix) on supported recommendations remediates a recommendation on multiple resources; without a Fix button there is no quick fix.
- **Enforce** deploys a policy to fix new noncompliant resources; **Deny** prevents creating them.
- IaC: change the module, not the resource — otherwise the next deploy reverts the fix.
- Resources are evaluated every 12 to 24 hours; an exemption can take up to 24 hours to take effect.

## Exempt (don't just ignore)
Recommendation → resource → **Exempt**: *Mitigated* or *Risk accepted*, with an optional expiration date (always set one). Mitigated exemptions count the resource as healthy, so the score increases.

## Track
Use continuous export for score history outside the portal.

## Gotchas
- Score drops when you onboard new subscriptions or enable plans that add recommendations — explain the trend, don't game it.
- Prefer exemptions over disabling a recommendation for everyone.

## Verify
- [ ] Weekly report: top 10 recommendations by risk with owners and due dates.
- [ ] Score trend recorded; exemptions all have expiry and reason.

## Checked

2026-10-28. Confirmed on the Defender for Cloud pages for implementing recommendations, exemptions and secure score: Fix button only where present, Enforce and Deny options, exemption types Mitigated and Risk accepted with optional expiry, exemptions take up to 24 hours, evaluation every 12 to 24 hours, Mitigated raises the score. Removed: both Resource Graph queries (property names not confirmed), score arithmetic, control names, the workbook name and the plan-dependency claim.

Method: documentation only; no commands were run.
