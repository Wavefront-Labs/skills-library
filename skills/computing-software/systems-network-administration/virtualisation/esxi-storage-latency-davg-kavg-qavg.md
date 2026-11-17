---
id: computing-software.systems-network-administration.virtualisation.esxi-storage-latency-davg-kavg-qavg
name: esxi-storage-latency-davg-kavg-qavg
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [davg-kavg-qavg, esxtop, vsphere-troubleshooting, storage-latency, queue-depth, vsphere-storage, vmware, vsphere]
level: advanced
status: docs-checked
description: "Pin down where ESXi storage latency comes from using esxtop DAVG, KAVG, QAVG and GAVG, queue depths (DQLEN, AQLEN), and the fixes for each pattern."
sources:
  - https://knowledge.broadcom.com/external/article/382249/using-esxtop-and-interpreting-esxtop-sta.html
  - https://knowledge.broadcom.com/external/article/344099/using-esxtop-to-identify-storage-perform.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Storage latency: DAVG, KAVG, QAVG, GAVG

esxtop views: `d` (adapter), `u` (device), `v` (VM disk). Use `u` first.

| Counter | Meaning | Concerning |
|---|---|---|
| **DAVG/cmd** | device latency: HBA → fabric → array → back | sustained > 10 ms is a documented concern |
| **KAVG/cmd** | time in the VMkernel | should stay near zero vs DAVG |
| **QAVG/cmd** | time queued in the VMkernel (part of KAVG) | high → examine queue statistics |
| **GAVG/cmd** | DAVG + KAVG: what the guest sees | per app SLA |
| ACTV / QUED | commands active at device / waiting in VMkernel | sustained high QUED = queueing |
| %USD | active commands as a share of queue depth | sustained high = queue saturated |
| ABRTS/s, RESETS/s | aborts and resets | any non-zero = path/array problem |

## Patterns
- **High DAVG, low KAVG**: array or fabric. Check array front-end/back-end busy, FC port
  errors, iSCSI network retransmits, wrong PSP (e.g. MRU on active/active array).
- **High KAVG/QAVG, low DAVG**: queuing in the host. Device queue depth too small for the
  load, or too many VMs per LUN. Raise HBA queue depth per vendor guidance, raise
  per-device outstanding I/O with the `esxcli storage core device set` options, or spread
  VMs across more LUNs.
- **Aborts/resets**: path flapping, array overloaded, firmware mismatch; check the
  VMkernel log for SCSI host status and sense codes.
- **High GAVG only on one VM**: snapshot chains, VM limits (IOPS limit via SIOC/policy),
  guest misalignment, single vCPU saturated.

## Batch capture for analysis
```sh
esxtop -b -d 5 -n 360 > /vmfs/volumes/DS01/esxtop-$(hostname)-$(date +%s).csv
```
Open in Windows perfmon or esxplot-like tools; filter on Physical Disk counters.

## Verify the fix
Repeat capture under the same workload: DAVG within array spec, QUED near 0, no aborts;
app latency matches.

## Checked
2026-10-31: Confirmed the GAVG = DAVG + KAVG relationship, DAVG/cmd, KAVG/cmd, GAVG/cmd
definitions and the sustained 10 ms guidance, QAVG as part of KAVG, and the ACTV, QUED and
%USD queue counters against Broadcom KBs 344099 and 382249. Replaced the per-counter
threshold column with the documented 10 ms guidance, and removed the DQLEN row, the
qlnativefc/lpfc parameter names and the H:0x5/H:0x8 host code names.
Method: documentation only; no commands were run.
