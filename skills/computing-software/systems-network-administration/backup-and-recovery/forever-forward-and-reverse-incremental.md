---
id: computing-software.systems-network-administration.backup-and-recovery.forever-forward-and-reverse-incremental
name: forever-forward-and-reverse-incremental
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [forever-incremental, reverse-incremental, forward-incremental, backup-chain, backup-methods, veeam, merge]
level: practitioner
status: docs-checked
description: "Choose between forward, forever forward and reverse incremental backup chains in Veeam: retention transforms, I/O cost, restore speed and the reverse incremental deprecation."
sources:
  - https://helpcenter.veeam.com/docs/backup/vsphere/backup_methods.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Forever forward and reverse incremental

**Goal:** pick a backup chain method that fits the repository's I/O and the restore patterns.

## Methods (Veeam Backup & Replication terminology)
| Method | Chain | Space and retention | Repository I/O | Restore speed |
|---|---|---|---|---|
| Forever forward incremental (FFI) | First full (VBK) plus forward incrementals (VIBs) | Saves space: only one full is stored; to meet retention the data of an incremental is injected into the full before the increment is deleted | Moderate; the full can fragment, so schedule the compact of full backup file operation (extra I/O) | Earliest restore point is fastest (it is always a full); other points comparable to FI |
| Forward incremental (FI) | Multiple fulls (VBKs), each followed by VIBs; fulls made by synthetic full or active full | Needs more space than the others; sometimes more restore points are stored than the retention setting because of FI retention specifics | Lowest; rises on synthetic-full days (backup storage) and active-full days (production storage) | Best for points that are not the earliest or latest, as chains are short |
| Reverse incremental (RI), deprecated | Full (VBK) plus reverse incrementals (VRBs) preceding it | Saves space: one full if no periodic fulls are scheduled | Heaviest: changed blocks are injected into the full and reverse increments are created; fragmentation and compact needed | Latest point fastest (always a full); earlier points slower |

## Choosing
- Regular full backups split the chain into shorter series, which lowers the chance of losing the whole chain and makes FI the most reliable method according to Veeam.
- FFI trades reliability for space (one long chain plus the merge into the full).
- Reverse incremental: in Veeam Backup & Replication 13 the option is deprecated and cannot be selected for new jobs; jobs from earlier versions that use it keep working after upgrade. Do not choose it for new designs.

## Gotchas
- FFI and RI both rewrite the full backup file, so budget for fragmentation and the scheduled compact of full backup file operation.
- Synthetic full days add I/O on the backup storage; active full days add load on production storage. Plan windows accordingly.
- For how each method retains restore points, see Veeam's per-method articles (Forward Incremental Backup Retention Policy, Forever Forward Incremental Backup, Reverse Incremental Backup) and Switching Between Backup Methods; they are linked from the Backup Methods page and were not read for this skill.

## Checked
2026-11-07. Read in full: Veeam Help Center "Backup Methods" (the entire fetched page, which is short; build 13.1.2.57, updated 2025-08-26). Removed because the page does not state them: the "about 3 I/O per changed block" figure, block-cloning (ReFS/XFS reflink) and deduplication-appliance advice, tape/offload advice, "whole chains deleted when the next chain satisfies retention", the health-check gotcha and the invented Verify step. Added: the reverse incremental deprecation in version 13. Linked per-method articles were not opened.
Method: documentation only; no commands were run.
