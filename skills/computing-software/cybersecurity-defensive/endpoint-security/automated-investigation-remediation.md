---
id: computing-software.cybersecurity-defensive.endpoint-security.automated-investigation-remediation
name: automated-investigation-remediation
category: computing-software
field: cybersecurity-defensive
product: endpoint-security
tags: [automated-investigation, air, defender-air, automation-levels, remediation-actions, action-center, edr-operations]
level: practitioner
status: docs-checked
description: "Use automated investigation and remediation (Defender AIR and equivalents): automation levels per device group, action center approvals, exclusions and auditing."
sources: ["https://learn.microsoft.com/en-us/defender-endpoint/automated-investigations", "https://learn.microsoft.com/en-us/defender-endpoint/automation-levels", "https://learn.microsoft.com/en-us/defender-xdr/m365d-action-center"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Automated investigation and remediation

Automated investigation (AIR) takes an alert, examines related entities (files, processes, services,
drivers, persistence, IPs), assigns verdicts and remediates - shrinking dwell time and SOC workload.

## Defender for Endpoint automation levels (per device group)
| Level | Behaviour |
|---|---|
| Full - remediate threats automatically | Remediation actions are performed automatically |
| Semi - require approval for all folders | Analyst approves all actions |
| Semi - require approval for core folders | Approval needed for remediation in core folders |
| Semi - require approval for non-temp folders | Approval needed for remediation in non-temp folders |
| No automated response | No automated investigation or remediation |

Set in Settings -> Endpoints -> Device groups. Start servers at semi-approval, workstations at full.

## Action center
Pending actions (approve/reject), history with undo for many actions (quarantine file, stop and quarantine,
remove persistence). Integrate approval notifications to the SOC channel.

## Tuning
- Indicators (allow) for false positives rather than turning automation off.
- Automation folder exclusions only for paths where remediation is unsafe (and log why).
- Review weekly: actions taken, undo rate (high undo = false positives).

## Other platforms
SentinelOne Storyline auto-mitigation, CrowdStrike Falcon Fusion workflows, Cortex XDR playbooks - same
principles: confidence threshold, scope by group, approval for servers, audit trail.

## Gotchas
- Auto-remediation on build servers or developer machines quarantines tools; dedicated groups with semi levels.
- Remediation without root cause analysis can leave the initial access path open; AIR closure is not incident closure for high-severity cases.

## Checked
2026-10-28. Confirmed in the automation levels page: the level names (full, semi for all folders, core folders, non-temp folders, no automated response). Removed: the "recommended by Microsoft" wording and the folder behaviour descriptions that did not match the page.
Method: documentation only; no commands were run.

## Verify
- [ ] Device groups assigned explicit automation levels.
- [ ] Monthly report of automated actions and undo rate.
