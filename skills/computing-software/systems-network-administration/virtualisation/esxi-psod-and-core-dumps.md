---
id: computing-software.systems-network-administration.virtualisation.esxi-psod-and-core-dumps
name: esxi-psod-and-core-dumps
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [psod, esxi-coredump, purple-screen, coredump-partition, netdump, vmkernel-zdump, vsphere-troubleshooting, vmware, esxi]
level: advanced
status: docs-checked
description: "Handle an ESXi purple screen: photograph it, make sure a coredump target exists (file/partition/network), extract the dump after reboot and read the backtrace for the culprit."
sources:
  - https://knowledge.broadcom.com/external/article?legacyId=1004250
  - https://knowledge.broadcom.com/external/article?legacyId=2004299
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ESXi purple screen (PSOD) and core dumps

**Goal:** turn a host crash into a root cause (driver, firmware, hardware or bug) instead
of "it rebooted".

## Before it happens: dump targets
```sh
esxcli system coredump partition get          # active partition?
esxcli system coredump file list              # ESXi 7+: file on a datastore/OSDATA
esxcli system coredump file add -d <datastore> -f <host>-dump
esxcli system coredump file set --smart --enable true
esxcli system coredump network set --enable true ; esxcli system coredump network check
```
A network coredump collector can also be configured as the target (see the ESXi coredump
documentation).

## When it happens
1. **Photograph the screen** (via BMC console screenshot): the first lines name the
   panic type (e.g. `PCPU 1 locked up`-style errors), the driver modules in the backtrace
   and the build number.
2. HA restarts VMs elsewhere. Leave the host in maintenance mode after reboot.
3. Check the BMC/IML/SEL log for hardware errors (memory ECC, PCIe AER) at that time.

## Extract and read the dump
- Easiest: export a vm-support bundle; it includes the core dumps.
- Manually from a partition: use the ESXi dump tools to copy the dump off the diagnostic
  partition (see KB 2004299).
- Patterns:
  - Driver module at the top of backtrace → check the driver/firmware HCL combo, update both.
  - `NMI` / hardware machine check (`MCE`) → hardware (memory DIMM, CPU); vendor diags.
  - Heartbeat/lockup style panics → often firmware/BIOS or hardware hang.
  - Known bug → search Broadcom KB with the exact panic string and build.

## Gotchas
- No dump target configured (common on SD-boot hosts) means no evidence; set it now.
- Repeated PSODs: keep the host out of the cluster until fixed; an unstable host
  causing repeated HA restarts is worse than reduced capacity.

## Verify
The coredump configuration shows an active target on every host; after the fix, the host
runs a burn-in period (e.g. 48 h) in maintenance mode or with test VMs before returning
to production.

## Checked
2026-10-31: PSOD interpretation (the `PCPU 1 locked up. Failed to ack TLB invalidate` class of errors, register and stack reading) confirmed in KB 1004250; the diagnostic coredump partition, its role in capturing PSOD output and the esxcli-based configuration confirmed in KB 2004299; `esxcli system coredump file add/set` and `esxcli system coredump network set` confirmed in the fetched pages. Removed unconfirmed specifics: the `--interface-name/--server-ipv4/--server-port` flags, the dump collector service claim, `#PF Exception 14`, specific driver module names, `var/core/vmkernel-zdump.*`, `esxcfg-dumppart -L` and the `vmkernel-log.1` file name.
Method: documentation only; no commands were run.
