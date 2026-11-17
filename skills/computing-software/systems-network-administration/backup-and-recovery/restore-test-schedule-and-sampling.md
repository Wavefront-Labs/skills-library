---
id: computing-software.systems-network-administration.backup-and-recovery.restore-test-schedule-and-sampling
name: restore-test-schedule-and-sampling
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [restore-test-schedule, restore-test, recovery-testing, audit-evidence, file-level-restore, achieved-rto, restore-test-report]
level: practitioner
status: draft
description: "Plan restore testing so every system is proven on a cadence: tier-based frequency, sampling of files, VMs, databases and SaaS, rotation, success criteria and evidence."
sources:
  - https://csrc.nist.gov/pubs/sp/800/34/r1/upd1/final
  - https://csrc.nist.gov/pubs/sp/800/84/final
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Restore test schedule and sampling

"The backup job succeeded" proves nothing about restore. NIST SP 800-34r1 requires testing
contingency capabilities; a schedule makes it routine instead of heroic.

## Cadence by tier (example)
| Tier | What | Frequency |
|---|---|---|
| Tier 0 (identity, backup server config, PKI) | full restore in isolated environment | quarterly |
| Tier 1 (critical apps, DBs) | full VM/app restore + app validation; DB restore + CHECKDB | monthly rotation, each system ≥ quarterly |
| Tier 2 | VM boot test (automated, e.g. SureBackup-style) | monthly sample, each system ≥ yearly |
| Files/shares | random file-level restores incl. old versions | weekly sample |
| SaaS (M365 mailbox, SharePoint site, Salesforce object) | item and bulk restore | quarterly |
| Offsite/immutable/tape copy | restore from the secondary copy, not primary | quarterly |
| Bare-metal / full site | DR exercise | yearly |

## Sampling
- Rotate so every protected system is tested within its tier interval (keep a list, tick off).
- Random file picks across age buckets (yesterday, last month, oldest retention point) to
  catch retention/catalog problems.
- Include at least one encrypted backup restored using escrowed keys per year.
- Test from **each** repository type (disk, object, tape, cloud).

## Success criteria per test
- Data restored completely and readable (checksum/compare with source where possible).
- App-level validation by owner (login, sample transaction, record counts).
- Time measured (achieved RTO) and recovery point age (achieved RPO) recorded vs targets.

## Evidence
Ticket or log per test: date, system, backup point used, repository, steps, duration, result,
issues and follow-ups. Auditors (ISO 27001 A.8.13, SOC 2, PCI) ask for exactly this.

## Automation
Use product features (Veeam SureBackup/SureReplica, dbatools Test-DbaLastBackup, PBS verify
jobs + scripted restores, restic `check --read-data-subset` + test restore) and keep humans for
app validation and the yearly full exercise.

## Verify
Coverage report: % of systems tested within interval per tier (target 100%), failed tests
with remediation tickets, RTO/RPO achieved vs target trend.
