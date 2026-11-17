---
id: computing-software.qa-testing-engineering.test-case-design.operational-acceptance-testing
name: operational-acceptance-testing
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [operational-acceptance-testing, oat, test-levels, backup-restore, disaster-recovery, installability, runbooks, monitoring-alerting]
level: practitioner
status: draft
description: "Run operational acceptance testing: installation, backup/restore, failover, monitoring and alerting, runbooks and maintenance tasks, before go-live."
sources:
  - https://www.istqb.org/certifications/certified-tester-foundation-level
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Operational acceptance testing (OAT)

**Goal:** operations/SRE accept that the system can be run, supported and recovered in production. ISTQB CTFL v4.0 2.2.1.

## Checklist
- **Deploy and rollback**: scripted deploy to a prod-like env; rollback to previous version works with data compatible.
- **Backup and restore**: take a backup, restore to a clean environment, verify data integrity and measure restore time against RTO; data loss against RPO.
- **Failover**: kill primary DB/node/AZ; service continues or recovers within target.
- **Monitoring and alerting**: dashboards exist; trigger each critical alert deliberately (stop a dependency, fill a disk) and confirm the alert reaches the on-call channel.
- **Logging**: logs are centralised, searchable, contain correlation ids, no secrets/PII.
- **Runbooks**: an operator not on the project follows the runbook for top incidents successfully.
- **Maintenance tasks**: certificate rotation, log rotation, scheduled jobs, patching with zero/acceptable downtime.
- **Capacity**: headroom confirmed by performance tests.
- **Security ops**: access control, secrets management, audit logging.

## Gotchas
- Alerts that were never fired in test often do not fire in production (wrong threshold, wrong channel).
- Restore tested on a tiny dataset hides real restore time.

## Verify
Signed OAT checklist with evidence (timings, screenshots of alerts received, restore logs).
