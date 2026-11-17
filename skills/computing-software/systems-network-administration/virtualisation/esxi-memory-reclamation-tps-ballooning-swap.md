---
id: computing-software.systems-network-administration.virtualisation.esxi-memory-reclamation-tps-ballooning-swap
name: esxi-memory-reclamation-tps-ballooning-swap
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [tps-balloon-swap, memory-overcommit, resource-management, esxtop, transparent-page-sharing, memory-ballooning, vmware, vsphere]
level: advanced
status: docs-checked
description: "Read ESXi memory reclamation (TPS, ballooning, compression, host swap) from esxtop and vCenter counters, know which states hurt, and fix overcommit properly."
sources:
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vsphere-resource-management/administering-memory-resources/sharing-memory-across-virtual-machines.html
  - https://knowledge.broadcom.com/external/article/323624/additional-transparent-page-sharing-mana.html
  - https://knowledge.broadcom.com/external/article/382249/using-esxtop-and-interpreting-esxtop-sta.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ESXi memory reclamation

ESXi reclaims memory in order of increasing pain as free host memory drops through the
**minFree** thresholds (states: high → clear → soft → hard → low).

| Technique | When | Guest impact |
|---|---|---|
| TPS (page sharing) | always, intra-VM; inter-VM only with salting off | none |
| Large page break-up | at clear/soft, enables TPS on large pages | minor |
| Ballooning (vmmemctl in Tools) | soft | guest swaps its own least useful pages; usually fine |
| Compression | hard | small latency |
| Host swapping (.vswp) | hard/low | **severe**: guest stalls on disk I/O |

## Inter-VM TPS
Disabled by default (salting): with the host default `Mem.ShareForceSalting=2` each VM gets
a unique salt, so only intra-VM page sharing happens. Re-enable only in trusted
single-tenant clusters (VDI) with `Mem.ShareForceSalting=0` or a common per-VM
`sched.mem.pshare.salt`; measure savings via the esxtop page-sharing counters.

## Read it in esxtop (`m` view)
- Header `PMEM /MB` free, and state (`high`, `clear`, `soft`, `hard`, `low`).
- Per VM: `MCTLSZ` (balloon size MB) and `SWCUR` (swapped now), plus the swap read/write,
  compression and cache counters (**any sustained swap read rate is user-visible**).
vCenter counters: Memory → Balloon, Swapped, Swap in rate, Compressed, Consumed vs Active.

## Fixing it
1. Find the cause: host overcommit (`sum(configured) / physical`) or a few VMs with
   **limits** set (a limit below configured memory forces ballooning/swap even on an idle
   host: check `Get-VM | Get-VMResourceConfiguration | ? MemLimitMB -ne -1`).
2. Remove accidental limits; right-size oversized VMs (Active ≪ Granted).
3. Rebalance with DRS or add hosts; reserve memory for latency-critical VMs (reservation
   also shrinks the .vswp file).
4. Keep Tools running everywhere: without the balloon driver, the host goes straight to
   compression/swap.

## Gotchas
- `Consumed` high with low `Active` is normal; ESXi does not reclaim until pressure.
- Swap on host cache (SSD) reduces but does not remove swap pain.
- Guest showing high memory while host balloons it is expected; don't "fix" in the guest.

## Verify
After changes, swap reads at 0 and `MCTLSZ` trending to 0 during peak; host state `high`.

## Checked
2026-10-31: Confirmed salting and the `Mem.ShareForceSalting=2` default (inter-VM TPS off,
intra-VM only, sched.mem.pshare.salt per-VM salt) against Broadcom KB 323624 and the
vSphere 8.0 "Sharing Memory Across Virtual Machines" page; the MCTLSZ and SWCUR counter
definitions and the GAVG/KAVG/DAVG latency relationships against Broadcom KB 382249.
Removed the 2014 date, the PSHARE/MB and SWR/s-SWW/s-ZIP/CACHEUSD counter names, and the
2 MB large-page figure.
Method: documentation only; no commands were run.
