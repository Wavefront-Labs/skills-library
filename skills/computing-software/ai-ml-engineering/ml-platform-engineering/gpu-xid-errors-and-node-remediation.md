---
id: computing-software.ai-ml-engineering.ml-platform-engineering.gpu-xid-errors-and-node-remediation
name: gpu-xid-errors-and-node-remediation
category: computing-software
field: ai-ml-engineering
product: ml-platform-engineering
tags: [ml-platform, gpu-monitoring, xid-errors, ecc-errors, dcgm-diagnostics, node-remediation, nvidia-smi, gpu-health]
level: practitioner
status: draft
description: "Detect and act on unhealthy GPUs: read Xid codes in kernel logs, ECC and row-remapping status, DCGM health checks and diagnostics, and cordon/drain/reset workflows."
sources:
  - https://docs.nvidia.com/deploy/xid-errors/index.html
  - https://docs.nvidia.com/deploy/a100-gpu-mem-error-mgmt/index.html
  - https://docs.nvidia.com/datacenter/dcgm/latest/user-guide/dcgm-diagnostics.html
  - https://docs.nvidia.com/datacenter/dcgm/latest/gpu-telemetry/dcgm-exporter.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# GPU Xid errors and node remediation

**Goal:** spot failing GPUs before they crash or silently slow distributed jobs, and take them out of service cleanly.

## Where errors show up
```bash
dmesg -T | grep -i xid                      # "NVRM: Xid (PCI:0000:3b:00): 79, ..."
nvidia-smi -q -d ECC,PAGE_RETIREMENT,ROW_REMAPPER
nvidia-smi --query-gpu=index,ecc.errors.uncorrected.volatile.total,retired_pages.pending --format=csv
```
dcgm-exporter exposes `DCGM_FI_DEV_XID_ERRORS` (last Xid code) and ECC counters - alert on them.

## Common Xids (see NVIDIA's Xid catalogue for the full list)
| Xid | Meaning | Usually |
|---|---|---|
| 13, 31, 43 | graphics engine exception / MMU fault / GPU stopped processing | application bug (bad memory access) - check the job first |
| 48 | double-bit ECC error | hardware; drain node |
| 63, 64 | ECC page retirement / row remapping event | hardware memory issue; reset needed to apply remap |
| 74 | NVLink error | hardware/interconnect |
| 79 | GPU has fallen off the bus | hardware/power/PCIe; node reboot, often RMA |
| 94, 95 | contained / uncontained ECC error | 94: app affected, GPU OK after; 95: reset required |
| 119, 120 | GSP firmware errors/timeouts | driver/firmware; reset, update driver |

Rule: an Xid that repeats on the same GPU across different jobs is hardware; one that follows a specific job across nodes is software.

## Health checks
```bash
dcgmi health -s a              # enable background health watches
dcgmi health -c                # check
dcgmi diag -r 1                # quick (seconds); -r 2 medium; -r 3 long (minutes, stress) - run on drained nodes
```
Run level 1 at node boot / before job start, level 3 when a node is suspected or after repairs.

## Remediation workflow (Kubernetes)
1. Detection (Xid alert, failed health check, or a straggler in a distributed job) -> `kubectl cordon <node>`.
2. `kubectl drain <node> --ignore-daemonsets --delete-emptydir-data` once running jobs checkpoint/finish.
3. Try `nvidia-smi -r -i <gpu>` (GPU reset, requires no processes on the GPU) or reboot the node.
4. Run `dcgmi diag -r 3`. Pass -> uncordon. Fail or recurrence -> replace instance (cloud) or RMA (on-prem).
Automate with node problem detector style checks or NVIDIA's health-check operators, labelling bad nodes so the scheduler avoids them.

## Gotchas
- Pending row remaps / retired pages only take effect after a GPU reset; until then errors recur.
- One sick GPU in a 512-GPU job slows or hangs every rank; per-rank step time monitoring catches "slow but not failed" GPUs.
- Keep driver, firmware and CUDA versions consistent across the fleet; mixed versions make Xid triage much harder.

## Verify
- [ ] Alerts exist for Xid, uncorrectable ECC and pending remaps.
- [ ] Cordon/drain/diag/uncordon runbook tested on one node.
- [ ] Repeat offenders tracked by GPU serial number.
