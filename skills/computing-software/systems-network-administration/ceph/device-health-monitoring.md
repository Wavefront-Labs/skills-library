---
id: computing-software.systems-network-administration.ceph.device-health-monitoring
name: device-health-monitoring
category: computing-software
field: systems-network-administration
product: ceph
tags: [ceph, devices, smart, device-health, diskprediction, locate-led]
level: practitioner
status: docs-checked
description: "Track physical drives in Ceph, enable SMART health scraping, and blink identify or fault LEDs."
sources:
  - https://docs.ceph.com/en/latest/rados/operations/devices/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
List devices known to the cluster:

```
ceph device ls
ceph device ls-by-daemon <daemon>
ceph device ls-by-host <host>
ceph device info <devid>
```

Locate a drive:

```
ceph device light on|off <devid> [ident|fault] [--force]
```

Health monitoring:

```
ceph device monitoring on
ceph config set mgr mgr/devicehealth/scrape_frequency <seconds>
ceph device scrape-health-metrics
ceph device get-health-metrics <devid> [sample-timestamp]
```

Failure prediction and alerts:

```
ceph mgr module enable diskprediction_local
ceph config set global device_failure_prediction_mode local
ceph device predict-life-expectancy <devid>
ceph device check-health
```

You can also set life expectancy by hand: `ceph device set-life-expectancy <devid> <from> [<to>]`. For the LED command the orchestrator must be available (`ceph orch status`); custom LED commands are stored with `ceph config-key set mgr/cephadm/blink_device_light_cmd`.

Automatic action is on by default. `mgr/devicehealth/self_heal` (enabled) marks `out` the OSDs on devices expected to fail within `mgr/devicehealth/mark_out_threshold` (default 4 weeks) and sets their primary affinity to 0, so data migrates away. `mon_osd_min_in_ratio` stops this cascading: if marking an OSD out would drop the `in` ratio below it, the module does not do so and the cluster raises `DEVICE_HEALTH_TOOMANY`. `mgr/devicehealth/warn_threshold` (default 12 weeks) controls `DEVICE_HEALTH`. SATA drives expose SMART, while SAS and NVMe metrics are collected through `smartctl`. The default `device_failure_prediction_mode` is `none`, and `local` requires the `diskprediction_local` module. `ceph device check-health` re-evaluates every stored life expectancy now.

## Checked

2026-11-03. Confirmed against: the Ceph Device Management page (docs.ceph.com/en/latest/rados/operations/devices/): device tracking, light, health monitoring, failure prediction, Health alerts, Automatic Migration.

Removed: nothing.

Method: documentation only; no commands were run.
