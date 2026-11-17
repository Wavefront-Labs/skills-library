---
id: computing-software.systems-network-administration.linux.nfs-client-diagnostics
name: nfs-client-diagnostics
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, nfs, mountstats, rpcdebug, nfsstat, nfsiostat, nfs-performance, nfs-troubleshooting]
level: advanced
status: docs-checked
description: "Diagnose slow or hanging NFS clients: nfsstat -c retransmissions, mountstats and nfsiostat per-op latency, rpcdebug kernel tracing, and reading 'server not responding' messages."
sources:
  - https://man7.org/linux/man-pages/man8/mountstats.8.html
  - https://man7.org/linux/man-pages/man8/nfsstat.8.html
  - https://man7.org/linux/man-pages/man8/rpcdebug.8.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# NFS client diagnostics

## Which mount and what options?
`nfsstat -m` prints information about each mounted NFS filesystem; start there to see how each mount is configured.

## Client counters
```bash
nfsstat -c            # client-side statistics (-c, --client)
nfsstat -m            # per-mount information (-m, --mounts)
```
Compare counters before and after a test run to see which counts change.

## Per-operation latency
```bash
mountstats /srv/share        # per-mount statistics from the client
nfsiostat 5 /srv/share       # iostat-like NFS view (see nfsiostat(8))
```
Read each tool's man page for what the RTT and execution-time columns mean on your nfs-utils version.

## Kernel tracing
```bash
rpcdebug -m nfs -s <flags>     # set NFS client debug flags (very verbose, goes to the kernel log)
rpcdebug -m nfs -c <flags>     # clear them again
rpcdebug -m rpc -s <flags>     # same for the RPC layer
```
`rpcdebug` sets and clears NFS and RPC kernel debug flags with `-m module`, `-s flags` and `-c flags`; the valid flag
names per module are in rpcdebug(8). Turn tracing off as soon as you have the sample.

## Verify
- [ ] The same counters or `nfsiostat` output taken after the fix show the symptom gone.

## Checked
2026-10-28. Confirmed in nfsstat(8), mountstats(8) and rpcdebug(8): `nfsstat -c`/`-m`, `rpcdebug -m/-s/-c`, existence of
nfsiostat. Removed as unconfirmed: `findmnt` options, retransmission interpretation, RTT versus exe reasoning, slot-table
sysctl, `nconnect` and kernel version, `umount -f -l`, `softerr`, tcpdump recipe, Kerberos checklist, `actimeo` advice,
the `rpcdebug ... all` flag names.
Method: documentation only; no commands were run.
