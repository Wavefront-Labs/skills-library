---
id: computing-software.digital-forensics-incident-response.log-analysis.stacking-and-long-tail-analysis
name: stacking-and-long-tail-analysis
category: computing-software
field: digital-forensics-incident-response
product: log-analysis
tags: [stacking, long-tail-analysis, frequency-analysis, threat-hunting, least-frequency-of-occurrence, velociraptor, kql, dfir]
level: practitioner
status: draft
description: "Hunt by stacking artefacts across many hosts (autoruns, services, processes, DNS) and investigating the rare long tail, with query patterns and pitfalls."
sources: ["https://www.sans.org/white-papers/37297/", "https://docs.velociraptor.app/docs/vql/", "https://learn.microsoft.com/en-us/kusto/query/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Stacking and long-tail analysis

**Goal:** find the attacker's footprint by counting how often each value occurs across the
estate; malicious items are usually rare (least frequency of occurrence).

## The method
1. Collect the same artefact from many comparable systems (same role/OS build): autoruns,
   services, scheduled tasks, running processes with paths and hashes, loaded drivers, DNS
   queries, user-agent strings, listening ports.
2. Normalise values (lowercase paths, strip user-specific segments like
   `\Users\<name>\`, version numbers if noisy).
3. Count occurrences per value (number of hosts, not number of events).
4. Review the rare end (1-3 hosts) first, plus anything unsigned or in user-writable paths.

## Query patterns
```kusto
// Defender/Sentinel: process images seen on few devices
DeviceProcessEvents
| where Timestamp > ago(14d)
| summarize Devices = dcount(DeviceId), Example = any(ProcessCommandLine) by SHA256, FileName, FolderPath
| where Devices <= 3
| order by Devices asc
```
```sql
-- Velociraptor notebook over a hunt of Windows.Sys.StartupItems / Autoruns
SELECT Entry, Image, count() AS Hosts
FROM source(artifact="Windows.Sysinternals.Autoruns")
GROUP BY Entry, Image
ORDER BY Hosts
```
```bash
# Plain CSVs: count distinct hosts per value
awk -F, '{print $3","$1}' autoruns_all.csv | sort -u | cut -d, -f1 | sort | uniq -c | sort -n | head -50
```

## Good stacking targets
Persistence (services ImagePath, Run keys, scheduled task actions, WMI consumers), process
names with paths and parent, named pipes, mutexes (memory hunts), network destinations per
process, DNS domains, installed software, local admin group members, SSH authorized keys on
Linux servers, cron entries, web server files by hash in webroots.

## Pitfalls
- Comparing unlike systems (servers vs workstations, different builds) floods the tail with
  legitimate differences; group by role first.
- Attackers that deploy everywhere (ransomware GPO, RMM tools pushed fleet-wide) will be
  *common*; also review "frequent but new" and "frequent but unsigned" items.
- Volume: start with high-signal artefacts; record what you dismissed and why so the hunt is
  repeatable.

## Self-check
Each rare item reviewed is labelled benign/suspicious with a reason, and the population and
grouping used for counting are documented.
