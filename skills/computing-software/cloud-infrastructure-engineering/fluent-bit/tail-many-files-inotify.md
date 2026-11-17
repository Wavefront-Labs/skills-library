---
id: computing-software.cloud-infrastructure-engineering.fluent-bit.tail-many-files-inotify
name: tail-many-files-inotify
category: computing-software
field: cloud-infrastructure-engineering
product: fluent-bit
tags: [fluent-bit, tail-input, inotify, sysctl, limitnofile, file-descriptors]
level: advanced
status: docs-checked
description: "Raise inotify and file descriptor limits so tail can watch many files, and know how queue overflow is handled."
sources: ["https://docs.fluentbit.io/manual/pipeline/inputs/tail"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Tailing many files

To monitor a large number of files on Linux, raise the inotify limits:

```text
sysctl fs.inotify.max_user_watches=LIMIT1
sysctl fs.inotify.max_user_instances=LIMIT2
```

Replace the limits with integers of your choosing. These revert on reboot unless written to a configuration file; the filename can vary with how Fluent Bit was installed. For example, with a file named `fluent-bit_fs_inotify.conf`:

```shell
mkdir -p /etc/sysctl.d
echo fs.inotify.max_user_watches = LIMIT1 >> /etc/sysctl.d/fluent-bit_fs_inotify.conf
echo fs.inotify.max_user_instances = LIMIT2 >> /etc/sysctl.d/fluent-bit_fs_inotify.conf
```

To raise the number of files the plugin can monitor, use a systemd override at `/etc/systemd/system/fluent-bit.service.d/override.conf` (or `override.yaml` for a YAML configuration, with `service: limitnofile: LIMIT`):

```text
[Service]
  LimitNOFILE=LIMIT
```

Create the override with `systemctl edit fluent-bit.service`.

**Queue overflow.** When the Linux inotify event queue overflows (`IN_Q_OVERFLOW`), Fluent Bit reconciles all monitored files: it detects rotated files by comparing inode numbers and file names and re-registers watches, resets offset tracking for truncated files, and retries watch registration for files that failed earlier, for example with `ENOSPC` when `fs.inotify.max_user_watches` is exhausted. No log lines are silently skipped, and higher kernel limits reduce the risk of overflow.

To use the file stat watcher instead of inotify, set `inotify_watcher: false` (default `true`).

Each monitored file gets its own buffer, which can significantly increase memory use (see `computing-software.cloud-infrastructure-engineering.fluent-bit.tail-buffer-tuning`).

## Checked

Method: docs-checked 2026-11-09 against the Fluent Bit docs tail input page (raw markdown, read in full).
