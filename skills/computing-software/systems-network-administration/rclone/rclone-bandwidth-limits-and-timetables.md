---
id: computing-software.systems-network-administration.rclone.rclone-bandwidth-limits-and-timetables
name: rclone-bandwidth-limits-and-timetables
category: computing-software
field: systems-network-administration
product: rclone
tags: [bwlimit, bandwidth, timetable, bwlimit-file, rate-limiting]
level: practitioner
status: docs-checked
description: "Limit rclone bandwidth globally, per direction, per file and on a weekday or time-of-day timetable."
sources: ["https://rclone.org/docs/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`--bwlimit` is in bytes per second, not bits. `--bwlimit 10M` limits both directions to 10 MiB/s; `0` means unlimited. Suffixes are B, K, M, G, T, P. Set directions separately as `UP:DOWN`, and use `off` for no limit:

```text
--bwlimit 10M:100k
--bwlimit 10M:off
```

## Timetables

A timetable is a list of `WEEKDAY-HH:MM,BANDWIDTH` entries separated by spaces or semicolons (use semicolons in Docker to avoid parsing trouble). `WEEKDAY` is optional and may be the full word or the first three letters. Bandwidth can be a single value or an `up:down` pair.

```text
--bwlimit "08:00,512k;12:00,10M;13:00,512k;18:00,30M;23:00,off"
--bwlimit "Mon-00:00,512;Fri-23:59,10M;Sat-10:00,1M;Sun-20:00,off"
```

Entries without a weekday apply to every day. The limit set by one entry holds until the next, so the first example is unlimited between 23:00 and 08:00. Divide a line speed in bit/s by 8 to get the value.

## Scope

The limit applies to data transfer on all backends and, for most, to directory listings too (not for ftp, sftp, storj). `--bwlimit-file` caps each file's rate (for example `1M`) and can combine with `--bwlimit`; with a schedule the file uses the entry in effect when its transfer starts. The limit can be changed on a running process through the rc call `core/bwlimit`. Servers such as `serve restic` respect `--bwlimit` for file transfers.

## Checked

2026-11-04: flags, defaults, option names and behaviour confirmed against the rclone.org documentation pages cited in sources (and the matching docs source on GitHub where the rendered page was cut off).

Method: documentation only; no commands were run.
