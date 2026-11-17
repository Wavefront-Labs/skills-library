---
id: computing-software.cloud-infrastructure-engineering.fluentd.in-tail-paths-globbing-and-rotation
name: in-tail-paths-globbing-and-rotation
category: computing-software
field: cloud-infrastructure-engineering
product: fluentd
tags: [cloud-infrastructure-engineering, fluentd, in-tail, tail, path, glob, follow-inodes, exclude-path, rotate-wait]
level: practitioner
status: docs-checked
description: "Configure in_tail file selection: path with globs and strftime, tag placeholder, exclude_path, glob_policy, follow_inodes against duplicates, and rotate_wait."
sources:
  - https://docs.fluentd.org/input/tail
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# in_tail paths and rotation
`in_tail` behaves like `tail -F`: on first configuration it starts at the end of a file; after rotation it reads the new file from the start and tracks the inode.

```
<source>
  @type tail
  path /var/log/httpd-access.log
  pos_file /var/log/fluent/httpd-access.log.pos
  tag apache.access
  <parse>
    @type apache2
  </parse>
</source>
```
- `tag`: `*` expands to the file path with `/` replaced by `.` (`path /path/to/file`, `tag foo.*` gives `foo.path.to.file`).
- `path`: comma-separated list; `*`, `**` and `strftime` (`/path/to/%Y/%m/%d/*`) add or remove watched files each `refresh_interval` (default 60s). `path_timezone` (1.8.1) overrides the system zone; `path_delimiter` (1.9.1) changes the separator (not `/`, `*`, `%`).
- `glob_policy` (1.17.0): `backward_compatible`, `extended` (`[]`, `?`), `always` (adds `{}`; needs a non-default `path_delimiter`).
- `exclude_path`: array, always comma separated, e.g. `["/path/to/*.gz", "/path/to/*.zip"]`.
- `follow_inodes true` (1.12.0): set it with `*` or strftime paths, or rotation duplicates logs.
- `limit_recently_modified`, `skip_refresh_on_startup` cut startup cost with many files.
- `rotate_wait`: seconds to keep reading the old file after rotation so late writes are not lost.
- `path_key`: adds the tailed path to each record.
- `enable_dir_watcher` with `dir_watcher_limit`: discover new files sooner than the refresh interval, at extra watch overhead.

## Checked

2026-11-04: read the fetched text of https://docs.fluentd.org/input/tail and confirmed: tag placeholder, path globbing, path_timezone, path_delimiter, glob_policy, exclude_path, follow_inodes, rotate_wait, dir watcher. Removed or reworded: the word "required" for follow_inodes (the page says should be set).

Method: documentation only; no commands were run.
