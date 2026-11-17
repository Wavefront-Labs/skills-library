---
id: computing-software.systems-network-administration.linux.reading-multipath-ll-and-failover
name: reading-multipath-ll-and-failover
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, multipath, multipath-ll, path-failover, multipathd, alua, path-checker, san]
level: advanced
status: docs-checked
description: "Read multipath -ll output (path groups, prio, active/enabled, failed/faulty paths), test path failover safely, and use multipathd show commands during SAN maintenance."
sources:
  - https://github.com/opensvc/multipath-tools/blob/master/multipathd/multipathd.8.in
  - https://github.com/opensvc/multipath-tools/blob/master/multipath/multipath.conf.5.in
  - https://github.com/opensvc/multipath-tools/blob/master/multipath/multipath.8.in
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Reading multipath -ll and testing failover

```
mpatha (36000d31000ec4a000000000000000012) dm-2 COMPELNT,Compellent Vol
size=500G features='1 queue_if_no_path' hwhandler='1 alua' wp=rw
|-+- policy='service-time 0' prio=50 status=active
| |- 3:0:0:1 sdc 8:32  active ready running
| `- 4:0:0:1 sde 8:64  active ready running
`-+- policy='service-time 0' prio=10 status=enabled
  |- 3:0:1:1 sdd 8:48  active ready running
  `- 4:0:1:1 sdf 8:80  failed faulty running
```
- Header: alias (WWID), dm device, vendor/product, size, `features` (`queue_if_no_path`/`no_path_retry` = I/O queues instead of erroring when all paths die).
- Path groups: the `status=active` group carries I/O; an `enabled` group is standby. `prio` is the path group priority.
- Path line: H:C:T:L (SCSI host:channel:target:lun), device, major:minor, then dm state (active or failed), checker state (`ready` can handle I/O, `faulty` unusable, `shaky` cannot handle I/O but can still be accessed, `ghost` stand-by, `i/o pending` being determined) and the offline state (running or offline).

## Live view
```bash
multipathd show paths format "%d %w %t %T %o %p"    # dev, wwid, dm state, checker, offline state, priority
multipathd show maps status
multipathd show topology
```
## Test failover (maintenance window)
```bash
multipathd fail path sdc                            # set the path into failed state
multipath -ll mpatha                                # sdc failed; I/O continues
multipathd reinstate path sdc                       # or wait for the checker
```
Or disable one switch port / fabric. Watch application I/O latency during the switch.

## Gotchas
- All paths in one group behind the same HBA = no redundancy; check H numbers span HBAs.
- `no_path_retry queue` (or `queue_if_no_path`) queues I/O forever when all paths are down, which can hang processes and shutdown — use a number of retries instead (see KNOWN ISSUES in multipath.conf(5)).
- Array vendor defaults are built in (`multipath -t` shows the configuration in use); override only on vendor advice.

## Verify
- [ ] Every map has ≥2 active paths across different HBAs; a path pull keeps I/O running and the path returns to `active ready`.

## Checked

Checked against multipath-tools master (multipathd/multipathd.8.in format wildcards and commands, multipath/multipath.conf.5.in; repository last pushed 2026-09-02).
Confirmed: wildcards %d %w %t %T %o %p %i %D; checker states ready, faulty, shaky, ghost, i/o pending; `%t` is active or failed; `%o` is the offline state; `multipathd fail path` and `reinstate path`; default `path_selector` `service-time 0`; `no_path_retry` semantics; `multipath -t`.
Removed unconfirmed claims: the sysfs offline/running test commands, the journalctl follow command and the ALUA prio remark. The example output block is illustrative.

Method: documentation only; no commands were run.
