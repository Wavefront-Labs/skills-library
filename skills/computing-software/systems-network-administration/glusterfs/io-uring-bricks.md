---
id: computing-software.systems-network-administration.glusterfs.io-uring-bricks
name: io-uring-bricks
category: computing-software
field: systems-network-administration
product: glusterfs
tags: [glusterfs, io-uring, linux-io-uring, posix, brick-performance]
level: advanced
status: docs-checked
description: "Enable io_uring for GlusterFS brick reads, writes and fsyncs with storage.linux-io_uring (glusterfs 9+), only while the volume is stopped."
sources:
  - https://raw.githubusercontent.com/gluster/glusterdocs/master/docs/Administrator-Guide/io_uring.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# io_uring on bricks

Requires glusterfs 9.0 or later. The option applies to the posix translator in the server-side brick process: reads, writes and fsyncs use io_uring calls instead of pread/pwrite-style syscalls.

```
gluster volume set testvol storage.linux-io_uring on
gluster volume set testvol storage.linux-io_uring off
```

The option can be changed only when the volume is not running, that is in the `Created` or `Stopped` state. Check the state with:

```
gluster volume status $VOLNAME
```

Stop the volume first if it is started (`gluster volume stop <VOLNAME>`), set the option, then start it again.

## Checked

2026-11-04: the glusterfs 9.0 gate, the posix translator behaviour, the set commands, and the Created or Stopped requirement were read against the glusterdocs page io_uring. Removed the claim that the default is off, which the page does not state.

Method: documentation only; no commands were run.
