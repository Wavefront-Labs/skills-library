---
id: computing-software.database-administration.oracle-database.cluster-verification-cluvfy-and-ahf
name: cluster-verification-cluvfy-and-ahf
category: computing-software
field: database-administration
product: oracle-database
tags: [database-administration, oracle-database, oracle, rac, cluvfy, ahf, orachk, tfa, grid-infrastructure, health-check]
level: advanced
status: docs-checked
description: "Check Oracle RAC and Grid Infrastructure health with cluvfy (pre/post stage and component checks) and AHF (ORAchk compliance, TFA diagnostic collection)."
sources:
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/cwadd/cluster-verification-utility-reference.html
  - https://docs.oracle.com/en/engineered-systems/health-diagnostics/autonomous-health-framework/ahfug/index.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cluster verification: cluvfy and AHF

## cluvfy
Ships with Grid Infrastructure (run from `Grid_home/bin`) as the grid owner.

Stage checks (before/after an operation):
```bash
cluvfy stage -pre crsinst -n node1,node2 -verbose -fixup        # before installing GI; -fixup generates root fix scripts
cluvfy stage -post crsinst -n all
cluvfy stage -pre dbinst -n node1,node2                         # before installing or creating an Oracle RAC database (see -help for options)
cluvfy stage -pre nodeadd -n node3                               # before adding a node
cluvfy stage -post hwos -n node1,node2                           # network and storage on the nodes
```
Component checks (troubleshooting):
```bash
cluvfy comp nodecon -n all -verbose          # interconnect/public connectivity
cluvfy comp ocr -n all
cluvfy comp vdisk -n all                     # voting files configuration and udev settings
cluvfy comp clocksync -n all                 # clock synchronization
cluvfy comp scan                             # SCAN name resolution and listeners
cluvfy comp asm -n all
cluvfy comp healthcheck -collect cluster -html   # best-practice report; -collect is cluster, database or asm (all three if omitted); text report without -html
```
`-fixup` generates fixup scripts to run as root where feasible; without `-verbose` only a summary is printed. `cluvfy stage <-pre|-post> <stage> -help` lists a stage's options. Stage names include crsinst, hwos, dbcfg, dbinst, hacfg, nodeadd, nodedel, acfscfg.

## AHF (Autonomous Health Framework)
Install/upgrade as root with `ahf_setup` (Oracle's installation and upgrade pages; Perl 5.10+ on Linux). It provides ORAchk/EXAchk and TFA (`tfactl`). Keep it current.

ORAchk: best-practice and known-issue compliance (patch recommendations, parameter checks, critical bugs):
```bash
orachk                      # interactive full run
orachk -profile dba         # subset: only Database Administrator checks (comma-separate profiles, e.g. dba,clusterware)
orachk -set "AUTORUN_SCHEDULE=3 * * 0"   # minute (optional) hour day month day_of_week: 03:00 every Sunday
orachk -set "NOTIFICATION_EMAIL=name@example.com"
orachk -autostart           # start the scheduling daemon (-autostop stops it)
```
Output: HTML report with a health score and FAIL/WARNING items, each linked to a MOS note.
Compare two runs: `orachk -diff <collection1.zip> <collection2.zip>` (collection ZIP files; `-force -showallcomparison` compares all targets).

TFA: diagnostic collection across nodes:
```bash
tfactl status
tfactl summary                      # cluster-wide status overview
tfactl analyze -last 1d              # recent errors in cluster-wide logs (also: -search "ora-00600" -last 8h)
tfactl diagcollect -last 2h          # collect diagnostics for the last 2 hours (-last accepts <=7 days or <=168 hours)
tfactl diagcollect                   # no options: pick an event from the menu; SRDC-linked events run the matching SRDC
```

## When to run what
| Moment | Run |
|---|---|
| Before install / add node / upgrade | `cluvfy stage -pre ...` |
| After change | `cluvfy stage -post ...`, `orachk` |
| Regularly | `orachk` scheduled, review the report |
| Incident | `cluvfy comp` for the suspected component, `tfactl diagcollect` |

## Verify
Latest pre/post cluvfy logs show PASSED (or documented exceptions), ORAchk runs on schedule, and TFA is running on all nodes.

## Checked
Date 2026-10-22. Oracle Database 19c Clusterware Administration and Deployment Guide (Cluster Verification Utility
reference) and Oracle Autonomous Health Framework User Guide (orachk profiles, scheduling, tfactl diagcollect/analyze).
Confirmed: stage and component names, -fixup / -verbose behaviour, healthcheck -collect and -html, orachk -profile dba,
-diff, AUTORUN_SCHEDULE and NOTIFICATION_EMAIL, -autostart/-autostop, tfactl analyze -last, diagcollect -last range.
Corrected: `tfactl diagcollect -since` and `-srdc dbperf` are not documented (diagcollect uses -last/-from/-to/-for and an
event menu for SRDCs). Removed unconfirmed: typical-failure list, "daily" autostart claim, `-d` on dbinst stage.
Not fully read: the last 47k characters of the CVU reference page. Source URL for AHF now points at the guide index.
Method: documentation only; no commands were run.
