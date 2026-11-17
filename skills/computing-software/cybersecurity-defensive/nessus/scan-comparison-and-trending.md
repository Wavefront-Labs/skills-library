---
id: computing-software.cybersecurity-defensive.nessus.scan-comparison-and-trending
name: scan-comparison-and-trending
category: computing-software
field: cybersecurity-defensive
product: nessus
tags: [nessus, scan-diff, scan-comparison, trending, vulnerability-states, scan-results, vulnerability-metrics]
level: practitioner
status: draft
description: "Compare vulnerability scans and trend results: Nessus diff/compare, Tenable VM new/fixed/resurfaced states, and building trend metrics that survive coverage changes."
sources: ["https://docs.tenable.com/nessus/Content/CompareScanResults.htm", "https://docs.tenable.com/vulnerability-management/Content/Explore/Findings/VulnerabilityStates.htm", "https://docs.tenable.com/security-center/Content/TrendAnalysis.htm"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Comparing scans and trending

## Nessus scan compare
Scan results > history > select two runs > Compare (Nessus Professional/Manager "Diff"). Shows
vulnerabilities only in one or the other. Useful for "what changed since the patch window?".
Both runs must use the same policy and targets; otherwise the diff measures config changes.

## Tenable VM / Security Center states
- **New**: first detected; **Active**: still present; **Fixed**: not seen on a later scan where
  the plugin ran with sufficient credentials; **Resurfaced**: fixed then detected again.
- Resurfaced findings indicate rollback, reimaging from old images, or flapping detections. Track
  them separately.
- Fixed requires the same plugin to run authoritatively on the asset; an unauthenticated rescan
  does not mark findings fixed (by design).

## Trend metrics that mean something
- Open critical/high by age bucket over time (0-30, 31-60, 61-90, 90+).
- New vs fixed per week (are you keeping up?).
- Mean time to remediate by severity, computed from first-seen to fixed.
- Normalise by asset count when coverage grows: findings per asset, or % assets with criticals.

Pytenable sketch for weekly new vs fixed:
```python
fixed = tio.exports.vulns(state=["FIXED"], last_fixed=int(week_ago))
new = tio.exports.vulns(state=["OPEN"], first_found=int(week_ago))
```

## Gotchas
- Plugin updates add detections for old issues; a spike in "new" may be new coverage, not new risk.
  Annotate plugin feed changes and large onboarding events.
- Decommissioned assets keep findings open until assets age out; set asset age-out rules.

## Verify
Trend chart reconciles: last week's open + new - fixed + resurfaced = this week's open (within
asset churn).
