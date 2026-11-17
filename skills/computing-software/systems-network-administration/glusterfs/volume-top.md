---
id: computing-software.systems-network-administration.glusterfs.volume-top
name: volume-top
category: computing-software
field: systems-network-administration
product: glusterfs
tags: [glusterfs, volume-top, read-perf, write-perf, list-cnt]
level: practitioner
status: docs-checked
description: "Find hot files and directories on a GlusterFS volume with gluster volume top (open, read, write, opendir, readdir, read-perf, write-perf), brick filter and list-cnt."
sources:
  - https://raw.githubusercontent.com/gluster/glusterdocs/master/docs/Administrator-Guide/Monitoring-Workload.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Volume top

```
gluster volume top VOLNAME open [brick BRICK] [list-cnt N]
gluster volume top VOLNAME read [brick BRICK] [list-cnt N]
gluster volume top VOLNAME write [brick BRICK] [list-cnt N]
gluster volume top VOLNAME opendir [brick BRICK] [list-cnt N]
gluster volume top VOLNAME readdir [brick BRICK] [list-cnt N]
gluster volume top VOLNAME read-perf [bs SIZE count N] [brick BRICK] [list-cnt N]
gluster volume top VOLNAME write-perf [bs SIZE count N] [brick BRICK] [list-cnt N]
```

What each reports:

- `open`: current and maximum open file descriptor counts, plus the most-opened files.
- `read` and `write`: files with the highest read or write call counts.
- `opendir` and `readdir`: directories with the highest open or read call counts.
- `read-perf` and `write-perf`: per-file throughput measured by a `dd` test with the given block size and count.

Notes:

- At most 100 results are shown; `list-cnt` accepts 0 to 100.
- `read` and `write` default to 100 files when no brick is named; the others show all bricks when none is named.
- The perf subcommands initiate a `dd` for the given count and block size and measure its throughput.

## Checked

2026-11-04. Confirmed against the glusterdocs Monitoring Workload page: all seven top subcommands and their syntax, the up to 100 results limit, list-cnt 0 to 100, the 100 file default for read and write, all bricks when none is named, and the dd based perf tests. Removed: the claim that dd generates I/O on the brick, which the page does not state.

Method: documentation only; no commands were run.
