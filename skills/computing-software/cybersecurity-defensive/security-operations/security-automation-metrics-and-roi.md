---
id: computing-software.cybersecurity-defensive.security-operations.security-automation-metrics-and-roi
name: security-automation-metrics-and-roi
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [automation-metrics, soar-automation, roi, soc-metrics, mttr, playbook-metrics]
level: practitioner
status: draft
description: "Measure security automation value: time saved per run, MTTA/MTTR change, automation coverage, failure rates and ROI reporting for SOAR programmes."
sources: ["https://docs.splunk.com/Documentation/SOAR/current/User/ROI", "https://www.tines.com/blog/", "https://www.sans.org/white-papers/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Automation metrics and ROI

## Core metrics
- **Executions** per playbook/story and success rate (failures need owners).
- **Time saved** = executions x (manual minutes - residual manual minutes). Measure manual
  minutes by timing analysts on 10 representative cases before automation, not guessing.
- **MTTA/MTTR** for automated vs non-automated incident categories, before and after.
- **Automation coverage**: % of alerts that receive automated enrichment; % of incident
  categories with response playbooks.
- **Auto-closure accuracy**: sample auto-closed alerts weekly; false negatives found in samples.
- **Analyst touch time** per alert type.

## Platform support
- Splunk SOAR ROI dashboard: set per-playbook "minutes saved" and cost per hour.
- Tines/XSOAR: export run data via API to SIEM and build dashboards.

## ROI statement
```
Hours saved per month = sum(playbook runs x minutes saved) / 60
Value = hours saved x loaded analyst cost
Cost = licences + engineering time + API costs
```
Report hours redirected (to hunting, engineering), not "headcount removed"; credibility matters.

## Gotchas
- Runs of trivial enrichment inflate numbers; weight by actual analyst minutes saved.
- Failed runs that analysts redo cost time; subtract.
- Faster MTTR can come from staffing changes; compare like-for-like periods.

## Verify
Quarterly report reconciles run counts with platform logs and includes sampled auto-closure QA results.
