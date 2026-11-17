---
id: computing-software.systems-network-administration.virtualisation.ceph-scrub-and-inconsistent-pgs
name: ceph-scrub-and-inconsistent-pgs
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [ceph-scrub, deep-scrub, ceph, pveceph, pg-inconsistent, ceph-health, proxmox]
level: advanced
status: docs-checked
description: "Schedule Ceph scrubs and deep scrubs to limit impact, read 'PGs not deep-scrubbed in time', and repair OSD_SCRUB_ERRORS / inconsistent PGs safely."
sources:
  - https://docs.ceph.com/en/latest/rados/configuration/osd-config-ref/
  - https://docs.ceph.com/en/latest/rados/troubleshooting/troubleshooting-pg/
  - https://docs.ceph.com/en/latest/rados/operations/health-checks/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ceph scrubbing and inconsistent PGs

- **Scrub** (default minimum interval 1 day): compares object metadata between replicas.
- **Deep scrub** (default every 7 days): reads all data and verifies checksums. Heavy I/O.

## Scheduling knobs (`ceph config set osd ...`)
| Option | Default | Typical change |
|---|---|---|
| `osd_scrub_begin_hour` / `osd_scrub_end_hour` | 0 / 0 (hours 0-23; no restriction) | 22 / 6 for night-only |
| `osd_scrub_begin_week_day` / `end_week_day` | 0 / 0 (0 = Sunday, 0-6) | restrict to some days if needed |
| `osd_deep_scrub_interval` | 7 days | longer on huge HDD clusters |
| `osd_scrub_min_interval` | 1 day | desired interval between scrubs of a PG |
| `osd_scrub_max_interval` | 7 days | scrub no less often than this |
| `osd_max_scrubs` | 3 | lower on HDD-only OSDs |
| `osd_scrub_load_threshold` | 10.0 (load divided by CPU count) | lower to keep scrubs off busy hosts |
| `osd_scrub_sleep` | 0 (seconds between chunks) | small values soften the impact |

Overly restrictive windows can leave PGs overdue and raise `PG_NOT_DEEP_SCRUBBED` / `PG_NOT_SCRUBBED` warnings. Widen the window or raise `osd_max_scrubs` until the backlog clears.

## Scrub errors
```sh
ceph health detail                         # OSD_SCRUB_ERRORS, PG_DAMAGED: pg 2.1f is active+clean+inconsistent
rados list-inconsistent-pg <pool>          # PGs of a pool that are inconsistent
rados list-inconsistent-obj 2.1f --format=json-pretty
```
Read the JSON to see which object and shard (OSD) is inconsistent and why.
- One OSD repeatedly at fault → check its disk and plan replacement.
- Then repair (the scrub's lead OSD chooses an authoritative copy; `pg repair` overwrites the inconsistent copy's digest with it, and for a replicated pool it marks the inconsistent copy as missing; recovery beyond that is outside `pg repair`):
  ```sh
  ceph pg repair 2.1f
  ```
- Re-run `ceph pg deep-scrub 2.1f` to confirm clean.
- For erasure-coded and BlueStore pools Ceph repairs automatically only when `osd_scrub_auto_repair` (default false) is true and no more than `osd_scrub_auto_repair_num_errors` (default 5) errors are found.

## Gotchas
- Periodic `active+clean+inconsistent` states can come from clock skew between monitor hosts; configure time sync (NTP) on them.
- The `pg repair` command will not solve every problem; check disks and logs of the OSDs involved.

## Verify
`ceph health detail` without scrub warnings; repaired PG back to `active+clean` after a new deep scrub.

## Checked

2026-10-26. Documentation checked: Ceph docs and option definitions (src/common/options) on ceph/ceph master (last commit 2026-10-25), pveceph(1) man page for PVE 9.2.13 and the pveceph.adoc source. Confirmed: scrub option defaults from the option definitions (osd_scrub_begin/end_hour 0/0, week day 0 = Sunday, osd_deep_scrub_interval 7d, osd_scrub_min_interval 1d, osd_scrub_max_interval 7d, osd_max_scrubs 3, osd_scrub_load_threshold 10.0, osd_scrub_sleep 0), PG_DAMAGED and scrub health checks, list-inconsistent-pg/obj, pg repair semantics, osd_scrub_auto_repair defaults. Corrected: osd_max_scrubs default is 3 (not 1) and osd_scrub_load_threshold is 10.0 (not 0.5); removed the unconfirmed awk pipeline and error-type names.

Method: documentation only; no commands were run.
