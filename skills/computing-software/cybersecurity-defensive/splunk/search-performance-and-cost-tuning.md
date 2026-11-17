---
id: computing-software.cybersecurity-defensive.splunk.search-performance-and-cost-tuning
name: search-performance-and-cost-tuning
category: computing-software
field: cybersecurity-defensive
product: splunk
tags: [splunk, performance-tuning, search-head, job-inspector, skipped-searches, scheduler-concurrency, summary-indexing, tstats, bucket-management, workload-management, splunk-enterprise-security, cost-optimisation]
level: advanced
status: draft
description: "Diagnose and fix slow or skipped Splunk searches: Job Inspector reading, scheduler concurrency limits, bucket/retention tuning, and summary indexing to cut recurring cost."
sources: ["Splunk Docs - Search job performance and search optimisation", "Splunk Docs - Configure the priority of scheduled reports", "Splunk Docs - Workload management", "Splunk .conf talks on SmartStore and bucket tuning (public conference material)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Search performance and cost tuning — find out why it's slow, not just that it is

**Goal:** diagnose why a search is slow or getting silently skipped, and fix the
actual bottleneck (bucket scanning, concurrency, inefficient SPL) rather than just
throwing more hardware or a longer schedule window at it.

## 1. Read the Job Inspector before guessing
Every search's Job Inspector (or `index=_audit`/`_internal` for scheduled jobs)
shows `scanCount` vs `eventCount` (how much got read vs how much mattered —
a huge gap means the search isn't using an index-time filter), time spent per
search command, and whether it hit `tstats` summaries or did a raw scan. Start
here, not with intuition — "add more search heads" is a common wrong fix for a
search that's scanning 50x the events it needs.

## 2. The usual suspects, in order of impact
1. **Leading wildcards and non-indexed-field filters** (`field=*foo`, filtering on a
   field extracted at search time before narrowing by indexed fields) force a full
   scan of the time range. Always filter on `index`, `sourcetype`, and any indexed
   field first; push field-based filtering as early in the pipeline as possible.
2. **Unaccelerated data models**: `tstats` without `summariesonly=true` or against
   a model whose acceleration hasn't finished scans raw data under the hood — check
   acceleration status under Settings → Data Models.
3. **Subsearches without a cap**: an unbounded subsearch returning thousands of
   values gets silently truncated (default 10,000 results/50,000 chars) and can be
   slow regardless — prefer `join`/lookup alternatives or pre-computed lookups for
   large value sets.
4. **`transaction`/`join` across huge result sets**: both buffer in memory; past a
   few hundred thousand events either is risky. Prefer `stats` with calculated
   fields where the logic allows it.

## 3. Scheduler concurrency and skipped searches
`index=_internal sourcetype=scheduler status=skipped` finds jobs that didn't run —
a silent detection/report gap, not a crash you'd notice. Common causes: too many
searches scheduled at round-number crons (`*/15 * * * *` everywhere) collide on
the same minute and exceed concurrency limits; a single long-running search above
its priority holds a slot. Stagger schedules (`7,22,37,52 * * * *` instead of
`*/15`), and set `priority`/`schedule_window` appropriately for business-critical
alerts so they preempt lower-priority reports.

## 4. Summary indexing / pre-computation for recurring heavy searches
If the same expensive raw search is run daily for a trend report, compute it once
on a schedule into a summary index (`collect` command) and have dashboards/reports
read the summary instead of recomputing from raw data each time a human opens a
panel. This trades ingest/storage cost for search-time cost — right call for
dashboards opened often; wrong call for a report run once a month.

## 5. Workload management and resource pools (Splunk Enterprise / Victoria)
On multi-tenant search heads, use workload management rules to cap CPU/memory per
search category (ad hoc vs scheduled vs real-time) so one analyst's exploratory
search can't starve scheduled security alerts. Real-time searches are the most
expensive per-result; prefer scheduled searches with a short lookback over
real-time unless sub-minute latency is a hard requirement.

## Gotchas
- A search that's fast in testing (small time range, warm cache) can be slow in
  production at full retention — always test performance over the real production
  time range, not "last 15 minutes."
- SmartStore (remote storage) buckets not yet cached locally add latency on first
  touch; a search spanning old, evicted buckets is slower than one over hot data —
  this is expected, not a regression, but budget for it in SLAs.
- Raising `max_searches_per_cpu`/concurrency limits without checking hardware
  headroom causes queueing and OOM elsewhere, not more throughput.
- `summariesonly=true` combined with poor acceleration coverage returns
  incomplete results silently — cross-check against a raw count periodically.

## Verify
- [ ] Job Inspector was checked and `scanCount`/`eventCount` ratio understood before
      any fix was applied.
- [ ] Scheduled searches are staggered, not all on round-number crons.
- [ ] `scheduler status=skipped` is monitored, not just crash/error logs.
- [ ] A recurring heavy dashboard search has a summary-indexing or acceleration
      plan if run more than a few times a day.

Related: computing-software.cybersecurity-defensive.splunk.spl-detection-searches,
computing-software.cybersecurity-defensive.splunk.data-onboarding-and-cim-mapping
