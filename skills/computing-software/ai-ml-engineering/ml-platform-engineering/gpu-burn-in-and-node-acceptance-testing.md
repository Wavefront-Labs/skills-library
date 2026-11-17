---
id: computing-software.ai-ml-engineering.ml-platform-engineering.gpu-burn-in-and-node-acceptance-testing
name: gpu-burn-in-and-node-acceptance-testing
category: computing-software
field: ai-ml-engineering
product: ml-platform-engineering
tags: [ml-platform-engineering, gpu-burn-in, node-acceptance-testing, dcgm-diagnostics, nccl-tests, gpu-health]
level: practitioner
status: draft
description: "Accept new GPU nodes before they join training: DCGM diagnostics levels, stress burn-in, NCCL bandwidth tests, memory/ECC checks, thermal limits and quarantine on failure."
sources:
  - https://docs.nvidia.com/datacenter/dcgm/latest/user-guide/dcgm-diagnostics.html
  - https://github.com/NVIDIA/nccl-tests
  - https://github.com/wilicc/gpu-burn
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# GPU burn-in and node acceptance testing

**Why:** at scale, a single bad GPU, link or cable slows or crashes a 1000-GPU job. Catch it before the node takes production work.

## Test sequence
1. **Inventory:** `nvidia-smi -q` matches expected GPU model, count, driver/CUDA versions, VBIOS; PCIe link width/speed correct; NVLink topology (`nvidia-smi topo -m`).
2. **DCGM diagnostics:** `dcgmi diag -r 3` (level 3: memory, PCIe bandwidth, stress tests, ~30 min) for new nodes; `-r 1`/`-r 2` as quick periodic checks. Any failure fails the node.
3. **Stress burn-in:** run sustained load (gpu-burn, DCGM targeted stress, or a real training benchmark) for hours; watch temperatures, clocks, power throttling and Xid errors in `dmesg`.
4. **Memory/ECC:** after burn-in, check `nvidia-smi -q -d ECC,PAGE_RETIREMENT` (or row remapping status); pending remaps or uncorrectable errors fail the node.
5. **Interconnect:** `all_reduce_perf -b 8 -e 8G -f 2 -g 8` (nccl-tests) within the node; then multi-node runs across the fabric comparing bus bandwidth with the expected NVLink/InfiniBand/EFA figures.
6. **Storage and network:** read throughput from the training filesystem, NIC link status.

## Operationalize
- Automate as a Kubernetes job/DaemonSet or Slurm prolog; label nodes `gpu-validated=true` only after passing; schedulers require that label.
- Failing nodes: cordon/drain, tag with failure reason, open a hardware ticket.
- Rerun quick checks periodically and after driver updates or reboots; track failure history per node to catch flaky hardware.

## Verify
- [ ] Acceptance report per node (tests, results, bandwidth numbers) stored; production pool contains only validated nodes.
