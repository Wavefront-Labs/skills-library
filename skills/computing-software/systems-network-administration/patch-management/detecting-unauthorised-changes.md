---
id: computing-software.systems-network-administration.patch-management.detecting-unauthorised-changes
name: detecting-unauthorised-changes
category: computing-software
field: systems-network-administration
product: patch-management
tags: [unauthorised-change, change-enablement, drift-detection, file-integrity-monitoring, audit-logs, cmdb]
level: practitioner
status: draft
description: "Detect changes made without a change record: sources (config drift, FIM, cloud audit logs, network config diffs), reconciling with the change schedule, and handling findings."
sources:
  - https://www.axelos.com/certifications/itil-service-management/itil-4-practitioner-change-enablement
  - https://csrc.nist.gov/pubs/sp/800/128/upd1/final
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Detecting unauthorised changes

NIST SP 800-128 (security-focused configuration management) and ITIL both expect you to
detect changes that bypass the process; they're a top cause of outages and a sign of
compromise.

## Detection sources
| Source | What it catches |
|---|---|
| Config management drift (Ansible check mode, Puppet/DSC reports) | config edited by hand |
| File integrity monitoring (AIDE, Wazuh, Tripwire, Defender FIM) | binaries/config files changed |
| Windows event logs (4719 audit policy, 4732 group membership, 7045 service installed) | privilege/system changes |
| Cloud audit (CloudTrail, Azure Activity Log, GCP Audit Logs) | console/API changes to infrastructure |
| Network config backups with diff (Oxidized/RANCID) | device config changes |
| Hypervisor events (vCenter events, PVE task log) | VM/host changes |
| Package history (dnf history, Windows update history) | software installed outside cycles |

## Reconcile
For each detected change: who (identity), what, when, where. Match against approved change
records active at that time (change ID in commit message, ticket field, or change window
calendar). Automate where possible: e.g. CloudTrail events with `userIdentity` not in the
automation role set during non-window hours → alert.

## Handling
1. Unmatched change → ticket to the owner; within 24 h either link to a retrospective
   change (approved after the fact, counted as unauthorised in metrics) or revert.
2. Suspicious (unknown identity, security settings) → security incident triage.
3. Repeat offenders/teams → process fix (standard change for frequent small tasks, better
   tooling) rather than only discipline.

## Reduce noise
Exclude expected automated changes (log rotation, AV definitions, patch agent writes) and
tag automation identities; tune FIM paths to config and binaries that matter.

## Gotchas
- Detection without reconciliation is just more alerts; staff the review.
- Break-glass changes during incidents are allowed but must be recorded afterwards.

## Verify
Weekly report: detected changes, matched %, unauthorised count by team, trend falling;
sample checks confirm detection sources cover critical systems.
