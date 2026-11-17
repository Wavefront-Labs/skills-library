---
id: computing-software.systems-network-administration.backup-and-recovery.restore-points-vs-day-based-retention
name: restore-points-vs-day-based-retention
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [restore-points, retention-policy, veeam-retention, backup-retention, gfs-retention, retention-math]
level: practitioner
status: docs-checked
description: "Choose between count-based and time-based backup retention using how Proxmox Backup Server prune, restic forget and AWS Backup lifecycle rules count, with their gotchas."
sources:
  - https://pbs.proxmox.com/docs/maintenance.html
  - https://restic.readthedocs.io/en/stable/060_forget.html
  - https://docs.aws.amazon.com/aws-backup/latest/devguide/creating-a-backup-plan.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Restore points vs day-based retention

**Goal:** retention behaves as intended when jobs run more or less often than planned.

## The two models
| Model | Counts | Risk |
|---|---|---|
| Restore points (keep last N) | number of backups | extra ad-hoc runs push old points out early; a job that runs more often keeps proportionally less history |
| Time (keep N days) | calendar age | if backups stop, old points keep expiring and you can end with very few |

## How the tools in the sources count
- **Proxmox Backup Server prune**: `keep-last`, `keep-hourly`, `keep-daily`, `keep-weekly`,
  `keep-monthly`, `keep-yearly`. `keep-last N` keeps the last N snapshots. The calendar options keep
  backups for the last N periods; when a period has several backups only the newest survives, and
  periods with no backups do not count toward N. Options are applied in the order listed, each
  covering its own time window, and the next considers only the older backups that remain. Weeks
  follow ISO weeks (Monday to Sunday). Snapshots with future timestamps are always kept. Pruning
  removes only snapshot metadata; data chunks stay on disk until garbage collection removes
  unreferenced ones after a grace period. The PBS docs mention a built-in prune simulator for
  testing a policy against a backup schedule.
- **restic `forget`**: `--keep-last n`; `--keep-hourly/daily/weekly/monthly/yearly n` (the most
  recent snapshot in each of the last n periods that contain a snapshot); `--keep-within duration`
  (all snapshots within the duration of the latest, for example `2y5m7d3h`). The policy is a union:
  a snapshot needs to match one option to be kept. Calendar options use natural boundaries (weeks
  are Monday 00:00 to Sunday 23:59). Policies apply per group of host, paths and tags unless
  `--group-by` changes it. `forget` removes the snapshots; `prune` (or `forget --prune`) then
  removes data only those snapshots referenced.
- **AWS Backup**: time-based lifecycle. The plan's **total retention period** is the number of days
  a resource is stored in AWS Backup (warm plus cold storage). Cold storage requires a total
  retention of 90 days or more, and AWS Backup recommends not moving a backup to cold storage
  until at least 8 days, because moving a full backup too early makes it create another warm full
  backup. The CLI example uses `Lifecycle` with `DeleteAfterDays`.
- Veeam and Azure Backup retention behaviour is not covered by the pages cited here; read the
  vendor documentation for your version.

## Choosing
- Use time-based retention when RPO or regulatory requirements are expressed in time ("keep 35 days").
- Use count-based where storage must be predictable and runs are fixed.
- With several runs per day, combine tiers: for example hourly or last-N for recent days, daily
  for a month, monthly for a year (tools such as PBS and restic let these options stack).

## Gotchas
- Deleting a snapshot is not the same as freeing space: in PBS and restic a later garbage
  collection or prune step reclaims the data.
- Changing from points to days changes storage use; recalculate capacity.

## Verify
After a month, list restore points and confirm the oldest date and count match the policy; simulate a multi-day outage of the job and check nothing unexpected expires.

## Checked
Method: docs-only read of cited pages, 2026-11-08

Confirmed against the Proxmox Backup Server maintenance (pruning) page, the restic forget page and the AWS Backup "Create a backup plan" page (total retention, cold storage 90 days, 8-day recommendation, `DeleteAfterDays`). The PBS prune simulator page itself contains only a title in text form, so the simulator is described from the maintenance page. Removed because no readable source states them: Veeam B&R v12 retention behaviour, GFS counting, Azure Backup, the `--keep-within 30d` example, "most tools keep at least the latest", and forever-incremental chain merge behaviour.
