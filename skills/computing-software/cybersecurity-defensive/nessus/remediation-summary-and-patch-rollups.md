---
id: computing-software.cybersecurity-defensive.nessus.remediation-summary-and-patch-rollups
name: remediation-summary-and-patch-rollups
category: computing-software
field: cybersecurity-defensive
product: nessus
tags: [nessus, remediation-report, patch-rollups, scan-results, reporting, tenable-vulnerability-management, vulnerability-remediation]
level: practitioner
status: draft
description: "Produce remediation summary reports from Nessus/Tenable scans: patch rollup consolidation, top remediations by risk reduction, per-owner action lists and exports."
sources: ["https://docs.tenable.com/nessus/Content/ScanResults.htm", "https://docs.tenable.com/vulnerability-management/Content/Explore/Findings/RemediationReport.htm", "https://docs.tenable.com/nessus/Content/Remediations.htm"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Remediation summary reports and patch rollups

Owners act on "install these 5 updates", not on 400 plugin findings.

## Patch rollups
Tenable consolidates superseded patch findings: when the latest cumulative update fixes many
CVEs, the scan reports the rollup (e.g. "KB5031361: Windows Server 2022 Security Update") and marks
older KBs as superseded. Enable "Display superseded patches" off (Advanced settings/report option)
to avoid duplicate work.

## Nessus remediations tab
In a scan's results, the **Remediations** tab lists actions ("Upgrade to OpenSSL 3.0.13 or later")
with count of vulnerabilities and hosts fixed by each. Export it via Report > custom with the
"Remediations" chapter.

## Tenable VM
- Explore > Findings: group by "Solution" or use the Remediation dashboards (Top 10 remediations by
  VPR, "Fix this to reduce X% of critical exposure").
- Remediation reports per tag (owner/business unit), scheduled export to CSV/PDF and emailed.

## Building the report
1. Scope by owner (asset tags) and SLA window (findings due this cycle or overdue).
2. Group by solution; sort by sum of risk (VPR/EPSS-weighted) or count of critical findings removed.
3. For each action: affected hosts, reboot required, change window, and validation method.
4. Track "risk reduced per action" to justify sequencing.

Example CLI export via pytenable:
```python
for f in tio.exports.vulns(severity=["critical","high"], tags=[("Owner","Windows Ops")]):
    key = f["plugin"].get("solution","").split("\n")[0]
    agg[key].add(f["asset"]["hostname"])
```

## Gotchas
- Non-patch findings (config, weak ciphers) have no rollup; list them separately.
- Hosts rescanned without credentials lose patch findings and look "fixed"; filter by
  authenticated scans.

## Verify
Pick three actions from the report, apply on a test host, rescan with credentials; findings
listed under those actions close.
