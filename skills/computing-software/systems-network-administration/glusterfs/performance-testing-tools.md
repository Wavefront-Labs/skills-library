---
id: computing-software.systems-network-administration.glusterfs.performance-testing-tools
name: performance-testing-tools
category: computing-software
field: systems-network-administration
product: glusterfs
tags: [glusterfs, performance-testing, fio, iozone, smallfile]
level: advanced
status: docs-checked
description: "Benchmark a GlusterFS volume with fio, iozone and smallfile, including distributed mode, dropping caches between phases, and the caveats of each tool."
sources:
  - https://raw.githubusercontent.com/gluster/glusterdocs/master/docs/Administrator-Guide/Performance-Testing.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Performance testing tools

- **fio** for large files and random I/O. Distributed mode:

```
fio --server --daemonize=/var/run/fio-svr.pid
fio --client=workload-generator.list --output-format=json my-workload.fiojob
```

Open port 8765 on generator hosts. Fio also has a libgfapi engine. Use time-limited tests; throughput is taken at the last thread's finish.

- **smallfile** for small files and metadata:

```
SMF="./smallfile_cli.py --top /mnt/glusterfs/smf --host-set h1,h2,h3,h4 --threads 8 --file-size 4 --files 10000 --response-times Y "
$SMF --operation create
$SMF --operation read
```

Other operations: append, rename, delete.

- **iozone** for large files (it also runs distributed, see below):

```
iozone -w -c -e -i 0 -+n -C -r 64k -s 1g -t 8 -F /mnt/glusterfs/f{0,1,2,3,4,5,6,7,8}.ioz
```

Distributed runs use `-+m ioz.cfg` (lines of `hostname directory iozone-pathname`), `export RSH=ssh`, and passwordless ssh. Avoid `-a`.

Drop caches between write and read phases on clients first, then servers:

```
sync; echo 1 > /proc/sys/vm/drop_caches
```

Use `gluster volume profile` and `gluster volume top` to examine results. Keep peak hardware utilisation around 60 to 80% and watch response times as well as throughput.

## Checked

2026-11-04. Confirmed against the glusterdocs Performance Testing page: fio server and client commands, port 8765, libgfapi engine, stonewalling and time-limit note, the smallfile example, the iozone example, -+m config format, RSH=ssh, discouraging -a, drop-caches ordering, profile and top, and the 60-80% utilisation target. Corrected: iozone is described by the page as strong at distributed testing, not single-host only.

Method: documentation only; no commands were run.
