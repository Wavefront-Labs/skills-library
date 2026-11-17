---
id: computing-software.cybersecurity-defensive.security-operations.detection-retirement-and-lifecycle
name: detection-retirement-and-lifecycle
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [detection-retirement, detection-lifecycle, detection-engineering, detection-health, content-management, detection-as-code]
level: practitioner
status: draft
description: "Manage the detection lifecycle from experimental to production to deprecated: health criteria, periodic review, retirement decisions and keeping history."
sources: ["https://github.com/palantir/alerting-detection-strategy-framework", "https://www.splunk.com/en_us/blog/security/detection-as-code.html", "https://github.com/SigmaHQ/sigma-specification"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Detection retirement and lifecycle

## States
- **Experimental**: runs, results go to a dashboard or low-priority queue; tuning in progress.
- **Test/Staging**: alerts to analysts with a flag; measured.
- **Production**: SLA-bound, owned, documented.
- **Deprecated**: disabled, kept in repo with reason; superseded-by link.
- **Retired/archived**: removed from SIEM; history preserved in git.

## Promotion criteria (example)
Two weeks experimental, < N alerts/day, true-positive or useful benign-true rate > 20%, triage notes
written, test dataset in CI, owner assigned.

## Periodic review (quarterly)
For each production detection gather: alert volume, TP/FP/BTP counts, mean triage time, last
true positive, data source health, ATT&CK technique relevance, overlap with other detections.

## Retirement reasons
- Data source decommissioned or schema changed (detection silently returns nothing - worst case).
- Superseded by better detection or vendor-native protection that prevents the behaviour.
- Persistent noise with no TP in 12 months and low technique relevance.
- Threat no longer relevant (software removed from estate).

## Process
1. Propose via PR changing status to deprecated with evidence.
2. Check coverage impact: ATT&CK layer before/after; if the technique loses all coverage, document
   accepted gap or replacement.
3. Disable in SIEM, keep 30-90 days, then remove; record `deprecated_date` and `reason`.

## Gotchas
- Zero alerts is not proof of value or uselessness; validate with test data before retiring.
- Never delete history: incident reviews may cite retired detections.

## Verify
Quarterly review output lists every production detection with a decision (keep/tune/deprecate)
and the coverage layer reflects deprecated items.
