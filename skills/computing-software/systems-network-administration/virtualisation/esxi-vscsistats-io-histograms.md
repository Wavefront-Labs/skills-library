---
id: computing-software.systems-network-administration.virtualisation.esxi-vscsistats-io-histograms
name: esxi-vscsistats-io-histograms
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [vscsistats, storage-performance, esxi, vmware, vsphere]
level: advanced
status: draft
description: "Collect per-virtual-disk I/O histograms on ESXi with vscsiStats (latency, I/O size, seek distance, outstanding I/O) to characterise a workload."
sources:
  - https://knowledge.broadcom.com/external/article?legacyId=1008205
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vsphere-monitoring-and-performance-8-0.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# vscsiStats I/O histograms

**Goal:** see what a VM's disk workload really looks like (block sizes, randomness, queue depth, latency distribution) to size storage or explain latency.

## Workflow (ESXi shell)
```bash
vscsiStats -l                          # list VMs: worldGroupID and per-disk handleID
vscsiStats -s -w 1234567               # start collection for a VM (all disks)
vscsiStats -s -w 1234567 -i 8200       # or a single disk handle
# ...let the workload run (collection auto-stops after 30 minutes)
vscsiStats -p latency -w 1234567
vscsiStats -p ioLength -w 1234567
vscsiStats -p all -w 1234567 -c > /tmp/app01-vscsi.csv   # CSV for spreadsheets
vscsiStats -x -w 1234567               # stop
vscsiStats -r                          # reset counters
```

## Histograms
| Type | What it tells you |
|---|---|
| `ioLength` | Block size mix (4K random OLTP vs 64K+ sequential backup) |
| `seekDistance` | Sequential (small distances) vs random |
| `outstandingIOs` | Queue depth the guest drives |
| `latency` | Distribution in microseconds; long tail reveals spikes averages hide |
| `interarrival` | Burstiness |

Each is split into reads and writes.

## Interpreting
- Many outstanding I/Os with high latency: storage saturated or queue limited; check device queue depth and DAVG.
- Low outstanding I/O with high latency: per-I/O latency problem (array, path, or network for NFS/iSCSI).
- Large I/O sizes during "slow" periods often coincide with backups or AV scans.

## Gotchas
- Stats are per virtual disk at the vSCSI layer, before the hypervisor storage stack; they do not distinguish array vs path latency (use esxtop for DAVG/KAVG).
- Run during the problem window; histograms averaged over idle time mislead.

## Verify
The CSV histograms reproduce the pattern seen by the application team (for example 8K random reads dominating with a latency tail over 20 ms).
