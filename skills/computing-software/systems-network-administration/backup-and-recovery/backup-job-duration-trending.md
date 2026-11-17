---
id: computing-software.systems-network-administration.backup-and-recovery.backup-job-duration-trending
name: backup-job-duration-trending
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [backup-duration-trend, backup-window, job-statistics, bottleneck-analysis, capacity-planning]
level: practitioner
status: draft
description: "Trend backup job durations to see backup window exhaustion coming: collect run times, read bottleneck stats, spot growth vs regressions, and act before overruns."
sources:
  - https://helpcenter.veeam.com/docs/backup/vsphere/realtime_statistics.html
  - https://helpcenter.veeam.com/docs/one/reporter/backup_job_historical_information.html
  - https://bp.veeam.com/vbr/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Backup job duration trending

## Collect
- Per job and per object: start, end, duration, processed GB, transferred GB, bottleneck.
- Sources: Veeam ONE "Backup Job Historical Information" / "Job duration" reports, Veeam REST sessions, or tool logs exported nightly to CSV or Prometheus.
- Keep at least 6 months.

## Read the trend
| Pattern | Likely cause | Action |
|---|---|---|
| Slow steady rise | Data growth | Capacity plan: more proxies/repo throughput, or split jobs |
| Sudden step up for one object | CBT reset, new active full, disk added, app churn | Check job log; reset expected? |
| Step up for all jobs same night | Storage/network change, AV scanning, firmware | Compare bottleneck stats before/after |
| Weekend spikes | Synthetic/active fulls, health checks, compact | Stagger them across days |
| High variance | Contention with other jobs or production | Re-stagger, I/O control |

## Bottleneck statistics
Veeam reports Source / Proxy / Network / Target busy %. The highest is where to invest: Source = production storage or transport mode; Proxy = CPU (compression); Network = links; Target = repository disks.

## Thresholds
Alert when a job's 7-day median duration exceeds 80% of its window, or one run is more than 2x its median.

## Gotchas
- Duration falls when a job starts failing early; trend together with success and processed GB.
- Moving VMs between jobs breaks per-job comparisons; trend per object as well.

## Verify
A monthly chart per job with window line drawn; any job above 80% has a ticket with a remediation plan.
