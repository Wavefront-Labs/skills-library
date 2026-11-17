---
id: computing-software.systems-network-administration.patch-management.vendor-risk-scores-vpr-and-trurisk
name: vendor-risk-scores-vpr-and-trurisk
category: computing-software
field: systems-network-administration
product: patch-management
tags: [vpr, trurisk, qds, vendor-risk-score, patch-prioritisation, vulnerability-management]
level: practitioner
status: docs-checked
description: "Use Tenable VPR and Qualys QDS/TruRisk scores in patch prioritisation: what drives them, why they change daily, how to combine with asset criticality and avoid black-box SLAs."
sources:
  - https://docs.tenable.com/vulnerability-management/Content/Explore/Findings/RiskMetrics.htm
  - https://docs.qualys.com/en/vmdr/3.19.0.0/threat/calculating_asset_risk_score.htm
  - https://docs.qualys.com/en/vmdr/latest/threat/qualys_trurisk.htm
  - https://www.first.org/epss/
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Vendor risk scores (Tenable VPR, Qualys QDS/TruRisk)

## What they are
- **Tenable VPR** (0.1-10.0): a dynamic companion to CVSS that Tenable updates to reflect the current threat landscape; higher means higher likelihood of exploit. Categories: Critical 9.0-10.0, High 7.0-8.9, Medium 4.0-6.9, Low 0.1-3.9. Values cannot be edited and are refreshed daily; vulnerabilities without CVEs get no VPR.
- **Qualys QDS** (1-100): per-QID score (Critical 90-100, High 70-89, Medium 40-69, Low 1-39) built from the highest Qualys Vulnerability Score (QVS) of the QID's CVEs plus threat intelligence (exploit code maturity, malware, threat actors, trending) and mitigating controls. Qualys recommends prioritising TruRisk-QDS of 70 or higher. **TruRisk** (0-1000): asset score = ACS (tag-based, highest tag value 1-5) times weighted averages of QDS per severity level, capped at 1000 (Low 0-499, Medium 500-699, High 700-849, Severe 850-1000).
- Other vendors offer similar threat-aware scores; check each vendor's documentation.

## Using them well
1. Prefer them over raw CVSS for ordering work; the CVSS base score does not track threat activity, VPR and QDS do.
2. Combine with **your** asset tier: vendor score says "how dangerous is this flaw", asset tier says "how bad if this box falls".
   Example rule (set your own numbers): `VPR >= 9 or KEV` on tier-1 internet-facing -> 7 days; `VPR 7-8.9` -> 30 days; rest -> normal cycle.
3. Set ACS / asset tags in the tool so TruRisk reflects reality; default ACS makes everything look equal.
4. Store the score at time of SLA assignment; a daily-changing score should not silently move a ticket's deadline backwards.

## Querying
Filter findings by the vendor score and your asset tag in each product's findings view, then export via API on a schedule into the ticketing/BI layer with both the vendor score and CVE/EPSS/KEV fields.

## Gotchas
- Scores are proprietary; auditors will ask how SLAs were derived. Document the thresholds and keep CVSS/EPSS/KEV alongside.
- Score drops (threat goes quiet) are not a reason to close or defer a KEV-listed finding.
- Different tools score the same CVE differently; pick one authoritative score per program.

## Verify
Top-N remediation list by vendor score x tier matches what analysts would pick manually on a sample; SLA breaches reported by tier.

## Checked
Date: 2026-10-27. Documentation: Tenable Vulnerability Management risk-metrics page (VPR range, bands, daily update, not editable), Qualys VMDR "Calculating TruRisk Score" page (version 3.19) and TruRisk prioritisation page (QDS ranges, ACS highest tag, TruRisk bands, formula cap 1000, QDS 70 recommendation). Removed the unconfirmed VPR driver list, the QDS-from-EPSS claim and both example filter queries.
Method: documentation only; no commands were run.
