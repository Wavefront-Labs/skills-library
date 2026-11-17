---
id: computing-software.messaging-and-integration.redpanda.production-readiness-checklist-health-and-host
name: production-readiness-checklist-health-and-host
category: computing-software
field: messaging-and-integration
product: redpanda
tags: [production-readiness, checklist, rpk-cluster-health, rpk-redpanda-check, xfs, raid, developer-mode]
level: practitioner
status: docs-checked
description: "Verify a Linux Redpanda cluster is production ready: license, cluster health, developer_mode and overprovisioned off, rpk redpanda check, version, resources and XFS disks."
sources:
  - https://docs.redpanda.com/streaming/current/deploy/redpanda/manual/production/production-readiness/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Critical checks, each with the command the page uses:

- **License:** `rpk cluster license info`, needed for enterprise features.
- **Health:** `rpk cluster info` should show no brokers down, and `rpk cluster health` should report `Healthy: true` with zero leaderless and zero under-replicated partitions.
- **Production mode:** `grep -E 'developer_mode|overprovisioned' /etc/redpanda/redpanda.yaml`. Both must be `false` or absent on every broker; if either is `true` the cluster is not in full production mode.
- **System requirements:** `sudo rpk redpanda check` (sudo because it reads `/proc` and `/sys`). It reports condition, required, current, severity (Warning or Fatal) and PASSED. Rows include ballast file, clock source `tsc`, listen backlog and max syn backlog >= 4096, XFS data directory, >= 10 GB free, 2048 MB free memory per CPU, max AIO events >= 1048576, NTP synced, swappiness 1 and tuned IRQ affinity, nomerges and scheduler.
- **Version:** every broker on the latest point release, via `/usr/bin/redpanda --version`.
- **CPUs and memory:** `journalctl -u redpanda | grep "System resources"` prints cpus, available and reserved memory.
- **Disks:** check `data_directory` in `redpanda.yaml` and `df -khT` on it. Multiple devices must be RAID-0 (other RAID levels can have significantly worse latencies; `mdadm --detail /dev/md0` shows the level). Use XFS formatted with `mkfs.xfs -m rmapbt=0`; ext4 if XFS is unavailable.

Also check tuners ran (`systemctl status redpanda-tuner`), `rpk iotune` ran with `/etc/redpanda/io-config.yaml` pointing at the data mount, and `rpk cluster self-test status` for disk performance.

## Checked

The checks, commands and expected outputs were confirmed on the Production Readiness Checklist page (Critical requirements), read in full.

Method: docs-checked 2026-11-09 against the Production Readiness Checklist page, read in full; no commands were run.
