---
id: computing-software.systems-network-administration.ceph.mclock-profiles
name: mclock-profiles
category: computing-software
field: systems-network-administration
product: ceph
tags: [ceph, mclock, osd, scheduler, qos, recovery]
level: advanced
status: docs-checked
description: "Select an mClock QoS profile for Ceph OSDs (balanced, high_client_ops, high_recovery_ops, custom) to trade client I/O against recovery."
sources:
  - https://docs.ceph.com/en/latest/rados/configuration/mclock-config-ref/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The mClock scheduler shares OSD I/O capacity between client work and background work (recovery, scrub). Profiles hide the low-level reservation, weight and limit values.

- `balanced`: the default.
- `high_client_ops`: favours clients over background operations.
- `high_recovery_ops`: favours background recovery.
- `custom`: you set the `osd_mclock_scheduler_*` values yourself.

Set a profile at runtime, cluster-wide or for one OSD:

```
ceph config set osd osd_mclock_profile high_recovery_ops
ceph config set osd.0 osd_mclock_profile high_recovery_ops
```

Capacity is determined automatically at OSD initialisation with the OSD bench tool, which sets `osd_mclock_max_capacity_iops_hdd` or `osd_mclock_max_capacity_iops_ssd` depending on the device type. If the measured value is not accurate, benchmark the drive yourself (for example with Fio) and override that option for one OSD (`ceph config set osd.N osd_mclock_max_capacity_iops_hdd <value>`) or globally.

Recovery settings such as backfills are locked while a built-in profile is active. To change them you must set `osd_mclock_override_recovery_settings` to true; the page lists the steps and says to reset it afterwards.

Use `high_recovery_ops` temporarily after a failure, then return to `balanced`.

Built-in profiles lock the low-level values: with `balanced`, `high_client_ops` or `high_recovery_ops` active, the reservation, weight and limit options such as `osd_mclock_scheduler_client_res`, `osd_mclock_scheduler_client_wgt` and `osd_mclock_scheduler_background_recovery_lim` cannot be changed. Commands report success but the values revert to the profile defaults. While any profile (including `custom`) is active, the recovery, scrub, delete and snap-trim sleep options are forced to 0 so the scheduler decides when to pick the next operation. The page does not recommend `custom` except for advanced users. To go from custom back to a built-in profile, first set the profile, then remove the custom values with `ceph config rm osd osd_mclock_scheduler_client_res`, and verify with `ceph config show osd.0`. `osd_mclock_override_recovery_settings` defaults to false. The page's override steps are: set it to true on all OSDs, set the desired option such as `osd_max_backfills`, wait a few seconds and verify with `ceph config show osd.N`, then set it back to false. It advises keeping the defaults on a running cluster. Profiles apply only when `osd_op_queue = mclock_scheduler`.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Confirmed against "mClock Config Reference" on docs.ceph.com: profile names and default, runtime `ceph config set` commands, locked options, sleep options set to 0, custom-to-built-in steps, override gating, capacity determination. Reworded the capacity sentence to what the page states.
