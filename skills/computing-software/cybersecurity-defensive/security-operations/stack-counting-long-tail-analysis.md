---
id: computing-software.cybersecurity-defensive.security-operations.stack-counting-long-tail-analysis
name: stack-counting-long-tail-analysis
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [threat-hunting, stack-counting, long-tail-analysis, frequency-analysis, least-frequency-of-occurrence, baselining, edr]
level: practitioner
status: draft
description: "Hunt with stack counting: aggregate artefacts across the estate, sort by rarity, and investigate the long tail of processes, autoruns, services and paths."
sources: ["https://www.sans.org/white-papers/the-who-what-where-when-why-and-how-of-effective-threat-hunting/", "https://www.threathunting.net/", "https://docs.velociraptor.app/docs/vql/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Stack counting and long-tail analysis

**Goal:** find the one malicious item among thousands of legitimate ones by counting how
many hosts share it. Attacker artefacts are usually rare; legitimate software is common.

## Method
1. Pick an artefact class that attackers must create: autoruns/run keys, services,
   scheduled tasks, process names + paths, loaded DLLs from user-writable paths, parent-child
   pairs, listening ports, browser extensions, WMI subscriptions.
2. Collect it from as many comparable hosts as possible (same OS and role; stacking servers
   with workstations hides outliers).
3. Normalise: lower-case paths, replace user names in paths (`%SystemDrive%\Users\*\AppData\...`),
   strip version numbers where they vary legitimately.
4. Count by the normalised value, sort ascending, review the bottom.

## Examples
Splunk, services created in 30 days:
```
index=wineventlog EventCode=7045 earliest=-30d
| eval img=lower(replace(ImagePath,"(?i)c:\\\\users\\\\[^\\\\]+","c:\\users\\*"))
| stats dc(host) as hosts values(host) as sample count by ServiceName img
| where hosts<=2 | sort hosts
```
KQL, process paths seen on few devices:
```
DeviceProcessEvents | where Timestamp > ago(14d)
| summarize Devices=dcount(DeviceId), Sample=any(DeviceName) by FolderPath, SHA256
| where Devices <= 3 | order by Devices asc
```
Velociraptor: run `Windows.Sys.StartupItems` or `Windows.System.Services` as a hunt across
the fleet, then stack the results in the notebook with `GROUP BY` and `count()`.

## Reviewing the tail
For each rare item check: signer, path (user-writable?), name mimicry (`svch0st.exe`,
`scvhost.exe`), creation time vs user activity, hash reputation, and whether it was
installed by software deployment tooling. Document benign explanations so the next hunt
can filter them (build an allowlist lookup).

## Gotchas
- Small fleets have a long tail of legitimate one-off software; segment by role and accept
  more manual review.
- Attackers deploying broadly (ransomware pre-staging, GPO persistence) are common, not
  rare; pair stacking with time-based views (what appeared everywhere this week?).
- Missing hosts in the collection make items look rarer than they are.

## Verify
Record hunt scope (hosts, time range, artefact), counts reviewed, findings, and new
allowlist entries; rerun later and compare tails for new entries.
