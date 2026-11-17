---
id: computing-software.systems-network-administration.patch-management.patch-coverage-and-latency-metrics
name: patch-coverage-and-latency-metrics
category: computing-software
field: systems-network-administration
product: patch-management
tags: [patch-metrics, patch-coverage, patch-latency, time-to-patch, mean-time-to-remediate, sla-compliance, nist-sp-800-40, patch-management]
level: practitioner
status: draft
description: "Measure patching per NIST SP 800-40r4: coverage, time-to-patch latency percentiles, SLA compliance by severity and asset group, data sources and pitfalls in the numbers."
sources:
  - https://csrc.nist.gov/pubs/sp/800/40/r4/final
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Patch coverage and latency metrics

**Goal:** a few numbers that show honestly whether patching works, by asset group, and
point at where it doesn't.

## Core metrics (NIST SP 800-40r4 categories: implementation, effectiveness, efficiency)
| Metric | Definition |
|---|---|
| Inventory coverage | Assets managed by the patching tool / assets in inventory |
| Patch coverage | Assets fully patched to the current baseline / managed assets |
| Time to patch (latency) | Release (or detection) date → verified install date, per vulnerability-asset pair |
| SLA compliance | % of remediations completed within the target for their severity |
| Open past SLA | Count and age of overdue vulnerability-asset pairs |
| Failure rate | Failed installs or rollbacks / attempted installs |
| Emergency response time | KEV or emergency advisory → fully remediated |

## Calculate latency properly
- Use **percentiles** (median, 90th, max), not averages: a few stragglers matter most.
- Start the clock at **vendor release** for efficiency, at **first detection** for
  operational teams; state which.
- Stop the clock at **verified** remediation (rescan), not at deployment, and only after
  any required reboot.
- Report per asset group and severity: internet-facing critical vs internal low look
  completely different and need different targets.

## Data sources
Vulnerability scanner (first-seen/last-seen/fixed dates), patch tool deployment logs,
CMDB for groups. Export weekly to a data store; trend over months.

## Pitfalls
- Assets missing from scanning look perfect: always show inventory coverage beside patch
  coverage.
- Re-imaged or renamed assets reset histories; use stable asset IDs.
- Accepted exceptions should be shown, not silently excluded.
- Version-based scanner findings on backported distro packages inflate open counts; fix
  detection rather than the metric.

## Verify
Metrics for last month reconcile with raw scanner exports for one asset group (spot
check); the dashboard shows inventory coverage, coverage, latency percentiles and overdue
counts per group.
