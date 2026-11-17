---
id: computing-software.systems-network-administration.linux.disk-benchmarking-with-fio
name: disk-benchmarking-with-fio
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, fio, ioping, disk-benchmark, iops, latency, storage-performance, direct-io]
level: advanced
status: docs-checked
description: "Measure storage honestly with fio: random/sequential jobs, direct I/O, iodepth and numjobs, latency percentiles, safe targets, and quick latency checks with ioping."
sources:
  - https://github.com/axboe/fio/blob/master/HOWTO.rst
  - https://github.com/koct9i/ioping/blob/master/ioping.1
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Disk benchmarking with fio

**Goal:** numbers that answer a question ("can this volume do 10k 4k random write IOPS at <2 ms p99?"),
not cache benchmarks.

## Safety first
Writing to a **raw device** destroys its data. Test a file on the filesystem, or a blank device you own.

## Core jobs
```bash
# random 4k read IOPS
fio --name=randread --filename=/srv/fio.test --size=10G --direct=1 --ioengine=libaio \
    --rw=randread --bs=4k --iodepth=32 --numjobs=4 --group_reporting --runtime=60 --time_based
# random 4k write with latency focus (database-like, sync writes)
fio --name=randwrite-sync --filename=/srv/fio.test --size=10G --direct=1 --sync=1 --ioengine=libaio \
    --rw=randwrite --bs=4k --iodepth=1 --numjobs=1 --runtime=60 --time_based
# sequential throughput
fio --name=seqread --filename=/srv/fio.test --size=10G --direct=1 --ioengine=libaio --rw=read --bs=1M --iodepth=16 --runtime=60 --time_based
# mixed 70/30
fio --name=mixed --rw=randrw --rwmixread=70 ...
```
Key flags: `--direct=1` bypass page cache (libaio only queues asynchronously for non-buffered I/O); `--ioengine=io_uring|libaio`;
`--iodepth` queue depth per job (no effect on synchronous engines); `--numjobs` parallel workers; `--sync=` selects synchronous
writes (`--fsync=N` syncs every N writes, but fio may skip it with non-buffered I/O); `--ramp_time=10` (seconds
before numbers are logged); `--output-format=json`.

## Read the output
`IOPS=`, `BW=`, and the **clat** (completion latency) percentiles; note the unit printed in the output. Averages hide pain; report p99/p99.9.
Watch `iostat -x 1` alongside for utilisation, queue size and await times.

## ioping (quick latency)
`ioping -c 10 /srv` (filesystem), `ioping -c 10 -D /dev/nvme0n1` (direct). Good for "is this NFS mount slow right now".

## Gotchas
- Test file smaller than RAM without `--direct=1` measures RAM.
- Cloud volumes with burst allowances inflate short tests — run long enough (check the provider's documentation for the volume type).
- Thin or newly provisioned volumes may be slower on first write — pre-fill them (`--rw=write` once) before measuring.
- SSDs can slow down when full or after sustained writes — precondition for serious testing.

## Verify
- [ ] Results repeatable across 3 runs; percentiles recorded with the exact job parameters.

## Checked

Checked 2026-10-26 against axboe/fio master (last commit 2026-10-21) HOWTO.rst and koct9i/ioping (ioping.1). Confirmed: option names (direct, ioengine, iodepth, numjobs, runtime, time_based, ramp_time, fsync, sync, rwmixread, output-format), libaio non-buffered queuing note, iodepth having no effect on synchronous engines, ioping -c and -D. Corrected: the synchronous-write example used --fsync with --direct=1, which fio may skip, so it now uses --sync=1; the sequential job gained an async engine so iodepth takes effect. Removed: vendor volume names (gp2, Azure) and the sample percentile line; the dead Google Cloud source link was dropped.

Method: documentation only; no commands were run.
