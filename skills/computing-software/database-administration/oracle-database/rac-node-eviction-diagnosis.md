---
id: computing-software.database-administration.oracle-database.rac-node-eviction-diagnosis
name: rac-node-eviction-diagnosis
category: computing-software
field: database-administration
product: oracle-database
tags: [database-administration, oracle-database, rac, real-application-clusters, node-eviction, css-misscount, ocssd, tfa, interconnect]
level: advanced
status: draft
description: "Diagnose why an Oracle RAC node was evicted or rebooted: network heartbeat vs disk heartbeat, ocssd and alert logs, OS resource starvation, and collecting TFA diagnostics."
sources:
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/cwadd/troubleshooting-oracle-clusterware.html
  - https://docs.oracle.com/en/engineered-systems/health-diagnostics/autonomous-health-framework/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# RAC node eviction diagnosis

Clusterware evicts (reboots or restarts the stack on) a node when it loses its **network
heartbeat** over the private interconnect beyond `misscount` (default 30 s), or its **disk
heartbeat** to the voting files beyond `disktimeout` (default 200 s), or when a local process
(ocssd, cssdagent/cssdmonitor) detects the node is hung.

## Collect first
```bash
tfactl diagcollect -srdc node_eviction        # or: tfactl diagcollect -from "2026-10-18 02:00:00" -to "2026-10-18 02:30:00"
```
TFA (part of AHF) gathers Clusterware, OS (OSWatcher), and database logs from all nodes.
Install AHF everywhere before you need it, with OSWatcher (or CHM) running.

## Logs to read (19c locations under the GI ADR)
- `<ORACLE_BASE>/diag/crs/<node>/crs/trace/alert.log` (Clusterware alert log) on **all** nodes.
- `ocssd.trc` around the time: look for
  - `clssnmPollingThread: node 2 at 50% heartbeat fatal, removal in 14.900 seconds` -> network heartbeat
  - `clssnmvDiskPingMonitorThread: voting file ... disk timeout` -> storage path to voting disks
  - `clssscMonitorThreads ... not scheduled for 15xxx msecs` -> the node itself was starved (CPU,
    memory, swapping)
- `cssdagent`/`cssdmonitor` traces for "reboot advisory".
- OS: `/var/log/messages`, `journalctl`, OSWatcher `vmstat`/`top`/`netstat` archives for the
  minutes before.

## Classify
| Evidence | Root cause area |
|---|---|
| missed network heartbeats from both sides | interconnect: switch, NIC bonding failover, MTU mismatch, firewall, packet loss (`netstat -s` reassembly failures) |
| disk timeout to voting files | SAN/multipath path failover taking > disktimeout, storage hang |
| threads not scheduled, high run queue, swapping | memory pressure (huge pages missing, SGA too big), runaway processes, VM host contention |
| NTP/chrony big time jump | time sync misconfiguration |

## Useful checks
```bash
crsctl get css misscount; crsctl get css disktimeout; crsctl get css reboottime
oifcfg getif                                  # which interface is cluster_interconnect
crsctl query css votedisk
ping -s 8972 -M do <other-node-priv-ip>       # jumbo-frame path test when MTU 9000
```
Do **not** raise `misscount` to hide problems except as directed by Oracle Support (vendor
multipath failover times sometimes justify it).

## Gotchas
- The evicted node's own logs may end abruptly; the surviving nodes' ocssd.trc explain the
  decision.
- Database-level `LMON`/`LMD` "IPC send timeout" and instance evictions are a different
  mechanism (instance membership), though causes overlap (interconnect).

## Verify
Root cause documented with log evidence from both nodes, the fix (network, storage, memory)
applied, and `crsctl stat res -t` / `olsnodes -s` show all nodes active with no recurrence over
the following weeks.
