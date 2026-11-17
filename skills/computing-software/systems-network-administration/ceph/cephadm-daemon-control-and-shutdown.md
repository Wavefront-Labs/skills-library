---
id: computing-software.systems-network-administration.ceph.cephadm-daemon-control-and-shutdown
name: cephadm-daemon-control-and-shutdown
category: computing-software
field: systems-network-administration
product: ceph
tags: [ceph, cephadm, orchestrator, daemon, shutdown, cluster-start]
level: practitioner
status: docs-checked
description: "Start, stop and redeploy cephadm daemons and shut down or start a whole cluster with cephadm cluster-shutdown and cluster-start."
sources:
  - https://docs.ceph.com/en/latest/cephadm/operations/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Single daemons and services:

```
ceph orch daemon stop <daemon-name>
ceph orch daemon start <daemon-name>
ceph orch daemon restart <daemon-name>
ceph orch stop <service-name>
ceph orch restart <service-name>
```

Redeploy or reconfigure:

```
ceph orch daemon redeploy <name> [--image <image>]
ceph orch daemon reconfig <name>
```

Whole cluster:

```
cephadm cluster-shutdown --fsid <fsid> --dry-run
cephadm cluster-shutdown --fsid <fsid> --yes-i-really-mean-it
cephadm cluster-start --fsid <fsid> --dry-run
cephadm cluster-start --fsid <fsid> --parallel 10
cephadm cluster-status --fsid <fsid>
```

Use `--dry-run` first on both. `--force` is available on shutdown.

Logs: `ceph -W cephadm` follows the cephadm log, `ceph -W cephadm --watch-debug` adds debug, `ceph log last cephadm` prints recent entries. For file logs run `ceph config set global log_to_file true` and `ceph config set global mon_cluster_log_to_file true`.

Details that prevent mistakes. Daemon names have the form `<type>.<id>`, such as `osd.0`, and `ceph orch ps` lists them; service names come from `ceph orch ls`, such as `mds.myfs`. Do not run `ceph orch restart` on an OSD service on a running cluster: it ignores CRUSH failure domains and parallel restarts can cause temporary data unavailability or, rarely, data loss. Shutdown requires `HEALTH_OK` with all PGs `active+clean` unless forced, then pauses the orchestrator, sets `noout`, fails CephFS file systems and stops hosts with the admin host last. State is saved to `/var/lib/ceph/<fsid>/cluster-shutdown-state.json`, which startup needs; by default 5 hosts start in parallel.

## Checked

2026-11-09. Confirmed against: the Ceph cephadm Operations page (docs.ceph.com/en/latest/cephadm/operations/): daemon and service control, redeploy and reconfig, cluster-shutdown and cluster-start, logging commands.

Removed: nothing; every command and number was found on the page.

Method: documentation only; no commands were run.

