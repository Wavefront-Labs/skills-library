---
id: computing-software.systems-network-administration.backup-and-recovery.live-failover-test-of-production
name: live-failover-test-of-production
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [live-failover-test, dr-test, planned-failover, failback]
level: advanced
status: docs-checked
description: "Plan a live production failover test: prior drills, planned failover for zero data loss, recovery point choice, validation and commit, with Azure Site Recovery examples."
sources:
  - https://learn.microsoft.com/en-us/azure/site-recovery/site-recovery-failover
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Live failover test of production

A real cutover of production to the DR site, run in an agreed window. Isolated tests prove VMs boot; only a live test proves users, integrations, licensing and capacity work. The examples below use Azure Site Recovery (ASR); adapt the ideas to your tool.

## Preconditions
- A successful drill (test failover) first. ASR says to run a disaster recovery drill before a full failover, and to run a successful test failover at least once every 180 days; it raises a failover-readiness health issue if there is none or the latest success is older than 180 days.
- Group machines into a recovery plan so they fail over together.
- Prepare connectivity before failover: for example, to reach Azure VMs over RDP or SSH after failover, complete the prerequisite tasks on the on-premises machine (for Linux, the SSH service set to start at boot and firewall rules allowing SSH).
- Approved change, named decision-maker and a rollback plan (your own process; not from the cited page).

## Choosing the failover mode and recovery point (ASR)
- **Planned failover** (Hyper-V) is the zero data loss option: the source VMs shut down first, the latest data synchronizes, then failover starts.
- **Regular failover** lets you choose a recovery point: latest processed (low RTO, no time spent processing unprocessed data), latest app-consistent, latest multi-VM processed, or latest multi-VM app-consistent (these two only for plans with multi-VM consistency enabled). Custom is only for single VMs.
- "Shut-down machine before beginning failover" asks ASR to shut down source VMs first; failover continues even if the shutdown fails. For Hyper-V VMs, shutdown tries to replicate data not yet sent.

## After failover
- Follow progress on the Jobs page; a recovery plan keeps running until all actions complete, even after an error.
- Sign in to the VM to validate it. You can still use Change recovery point to pick a different point.
- Commit when ready: Commit deletes all recovery points held by the service, and Change recovery point is then unavailable. Do not commit until validation passes.

## Gotchas
- Plan failback with the same care as failover (your own process; the cited page covers failover only).

## Verify
Record measured RTO and data loss (zero expected for planned failover) and capture issues in an after-action report.

## Checked

2026-11-09. Confirmed against the ASR "Run a failover from on-premises to Azure" page (180-day test rule, connectivity prerequisites, recovery plan failover options, shut-down option, validation, change recovery point, commit, planned failover for Hyper-V). Partial read; the page tables were summarised. Removed: NIST SP 800-34 and Broadcom Live Recovery sources (not fetched or out of scope), SRM and Zerto modes, the T-7 timeline, TTL lowering, abort time thresholds (60 minutes, 2 hours), weekend window length and hidden dependency list, and the database switchover advice.

Method: documentation only; no commands were run.
