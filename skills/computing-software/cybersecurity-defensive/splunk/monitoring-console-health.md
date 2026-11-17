---
id: computing-software.cybersecurity-defensive.splunk.monitoring-console-health
name: monitoring-console-health
category: computing-software
field: cybersecurity-defensive
product: splunk
tags: [splunk, splunk-architecture, monitoring-console, dmc, health-check, indexing-queues, platform-alerts, splunk-internal-logs, skipped-searches]
level: practitioner
status: draft
description: "Use the Splunk Monitoring Console to find blocked queues, skipped searches, disk and licence issues across a distributed deployment, with platform alerts."
sources: ["Splunk Docs - Monitoring Splunk Enterprise (About the Monitoring Console)", "Splunk Docs - Platform alerts", "Splunk Docs - Troubleshoot indexing performance"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Monitoring Console health checks

**Goal:** know before analysts do that Splunk is dropping, delaying or failing to search data.

## Setup
1. Run the Monitoring Console (MC) on a dedicated instance (or the licence manager / cluster
   manager in small estates), never on a busy search head.
2. Settings > Monitoring Console > General Setup: switch to **Distributed mode**, add every
   instance as a search peer, assign server roles correctly, Apply.
3. Enable **Platform Alerts** (Settings > Searches): near-critical disk, abnormal
   instance state, saturated indexing queues, missing forwarders, expiring licence.
   Route them to the platform team, not the SOC queue.

## The five checks that matter
| Check | MC view / search |
|---|---|
| Indexing queues blocked | Indexing > Performance > Indexing Performance: Deployment. The rightmost queue that is full is the bottleneck (often disk I/O). |
| Skipped searches | Search > Scheduler Activity, or `index=_internal sourcetype=scheduler status=skipped | stats count by savedsearch_name reason` |
| Forwarder silence | Forwarders > Forwarder Monitoring (enable forwarder monitoring data collection). |
| Latency | `| tstats max(_indextime) as it max(_time) as t where index=* by index sourcetype | eval lag_s = it - t` |
| Disk | Indexing > Indexes and Volumes. |

Run **Health Check** (MC > Health Check) after upgrades; it runs Splunk best-practice checks
(Transparent Huge Pages, ulimits, clock skew).

## Diagnosing a blocked queue
```
index=_internal source=*metrics.log group=queue blocked=true
| timechart count by name
```
- `parsingqueue` blocked alone: heavy regexes/props on that tier.
- `indexqueue` blocked: storage too slow or full.
- All queues blocked on forwarders: indexers refusing connections (check `tcpin_connections`).

## Gotchas
- MC only knows instances you added; a new indexer not added is invisible.
- Wrongly assigned server roles give empty panels, not errors.
- `ulimit -n` and Transparent Huge Pages are the most common Linux health-check failures.

## Verify
- [ ] Distributed mode lists every instance with the right roles.
- [ ] Platform alerts enabled and delivered to a monitored channel.
- [ ] A weekly review of skipped searches and blocked queues exists.
