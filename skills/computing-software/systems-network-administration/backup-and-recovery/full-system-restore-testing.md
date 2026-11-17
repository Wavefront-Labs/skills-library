---
id: computing-software.systems-network-administration.backup-and-recovery.full-system-restore-testing
name: full-system-restore-testing
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [full-system-restore, restore-testing, isolated-recovery-environment, surebackup, virtual-lab, rto-measurement, restore-sandbox]
level: advanced
status: draft
description: "Test full system restores: restore whole VMs or physical servers into an isolated network, boot and verify services and apps, measure time against RTO, and record evidence."
sources:
  - https://helpcenter.veeam.com/docs/backup/vsphere/surebackup_job.html
  - https://csrc.nist.gov/pubs/sp/800/84/final
  - https://csrc.nist.gov/pubs/sp/800/34/r1/upd1/final
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Full system restore test

**Goal:** prove a complete server (OS, application, data) can be rebuilt from backup within its RTO.

## Scope and cadence
- Every critical system at least annually; Tier 0 (identity, backup server itself) and Tier 1 quarterly.
- Rotate through restore methods: VM image restore, instant recovery, bare-metal restore to spare hardware, cloud restore.

## Isolated environment
- Separate network segment or virtual lab with no route to production (avoid duplicate hostnames/IPs and AD conflicts).
- Include dependencies the system needs (a restored DC and DNS from the same point in time, database servers).
- Veeam SureBackup automates this: application group (dependencies) plus virtual lab with a proxy appliance for masquerade IP access.

## Procedure
1. Record start time.
2. Restore the system (and dependencies) from a chosen restore point.
3. Boot; check: OS boots cleanly, services running, event logs clean, application responds (login, query, test transaction), data current to the restore point.
4. Record end time when the application owner confirms function.
5. Tear down the environment.

## Evidence
Test record: system, restore point date, method, start/end times, achieved RTO vs target, achieved RPO (restore point age), issues found, sign-off. Keep for audit (ISO 27001, SOC 2 ask for this).

## Gotchas
- Restoring a DC into a network with production DCs causes USN/replication chaos; isolate strictly.
- Licence activation, hardware-bound keys and certificates may fail on restored copies; note them in the DR runbook.
- Physical restores are slowest; include them occasionally to keep skills.

## Verify
Achieved RTO is within target for each tested system; misses produce tracked actions.
