---
id: computing-software.messaging-and-integration.redpanda.linux-open-file-limits
name: linux-open-file-limits
category: computing-software
field: messaging-and-integration
product: redpanda
tags: [linux, file-descriptors, limitnofile, systemd, sysctl, partition-limits]
level: advanced
status: docs-checked
description: "Check and raise the Linux open file limits that cap Redpanda partitions: LimitNOFILE in a systemd drop-in, fs.file-max, fs.nr_open, and the Refusing to create log warning."
sources:
  - https://docs.redpanda.com/streaming/current/deploy/redpanda/manual/linux-system-tuning/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Each partition replica uses several file descriptors, and each client or internal RPC connection uses another. At the limit a broker cannot open files or accept connections. `rpk redpanda tune` does not change any of these limits.

**Three limits:** `fs.file-max` (kernel-wide handle cap), `fs.nr_open` (ceiling for any per-process limit) and the per-process `RLIMIT_NOFILE` (what `ulimit -n` reports; the soft limit is what Redpanda runs with).

**Packaged default.** The `redpanda` systemd service sets `LimitNOFILE=800000` (soft and hard). Containers or custom unit files get whatever starts the process. Change it with a drop-in, not the packaged unit:

```bash
sudo systemctl edit redpanda
```
```ini
[Service]
LimitNOFILE=<limit>
```
```bash
sudo systemctl restart redpanda
```

A value above `fs.nr_open` is capped to it. To persist kernel limits, put them in `/etc/sysctl.d/99-redpanda.conf` (`fs.file-max`, `fs.nr_open`) and run `sudo sysctl --system`.

**Check**
```bash
sysctl fs.file-max fs.nr_open
cat /proc/sys/fs/file-nr
grep 'Max open files' /proc/$(pidof redpanda)/limits
journalctl -u redpanda | grep 'File handle limit'
```

**Effect on partitions.** Redpanda caps the cluster's partition replicas using this limit. Only the controller leader checks it, using its own soft limit for every broker, so set the same limit everywhere. A refused request logs a warning starting `Refusing to create` and ending `would exceed FD limit <value>` on the controller leader, found via the `Controller ID` field of `rpk cluster health`.

## Checked

2026-11-04. All limits, the 800000 default, drop-in steps, check commands and the partition-creation behavior were confirmed on the Linux System Tuning page.

Method: documentation only; no commands were run.
