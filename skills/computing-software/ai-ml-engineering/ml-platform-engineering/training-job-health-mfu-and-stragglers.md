---
id: computing-software.ai-ml-engineering.ml-platform-engineering.training-job-health-mfu-and-stragglers
name: training-job-health-mfu-and-stragglers
category: computing-software
field: ai-ml-engineering
product: ml-platform-engineering
tags: [ml-platform, gpu-monitoring, mfu, straggler-detection, training-throughput, distributed-training, nccl-flight-recorder]
level: practitioner
status: draft
description: "Monitor large training jobs: tokens/sec and model FLOPs utilization (MFU), per-rank step time to catch stragglers, hang detection and dashboards that page on real problems."
sources:
  - https://arxiv.org/abs/2204.02311
  - https://arxiv.org/abs/2205.05198
  - https://pytorch.org/docs/stable/torch.compiler_troubleshooting.html
  - https://pytorch.org/tutorials/prototype/flight_recorder_tutorial.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Training job health: MFU and stragglers

**Goal:** know within minutes when a multi-node training job is slower than it should be, and which node is at fault.

## Throughput and MFU
- Log **tokens/sec** (or samples/sec) per step and globally.
- **Model FLOPs Utilization** (PaLM paper): achieved model FLOPs / peak hardware FLOPs. For decoder transformers, training FLOPs per token ~= `6 * N_params` plus attention (`12 * n_layers * d_model * seq_len`):
```python
flops_per_token = 6 * n_params + 12 * n_layers * d_model * seq_len
mfu = tokens_per_sec * flops_per_token / (n_gpus * peak_flops_per_gpu)   # peak e.g. dense bf16 spec of the GPU
```
- Well-tuned large LLM training typically reports MFU around 35-55%; much lower suggests communication overhead, input stalls, too-small micro-batches, or recomputation you didn't count. Note HFU (hardware FLOPs incl. activation recomputation) is higher than MFU by design.
- MFU drop mid-run with no config change = something broke (slow node, network, storage).

## Per-rank step time (stragglers)
In synchronous data parallelism every step waits for the slowest rank. Log step time per rank (or time spent waiting in the all-reduce):
- One rank consistently slower -> bad GPU (thermal throttling, ECC, PCIe), noisy neighbour, slow local disk for its data shard.
- All ranks slow together -> network/storage/global issue.
Check that rank's node: `nvidia-smi -q -d PERFORMANCE` (clock throttle reasons), DCGM `DCGM_FI_DEV_SM_CLOCK`, NIC counters.

## Hangs
- Set a collective timeout in `init_process_group(timeout=timedelta(minutes=10))` so hangs fail instead of idling forever.
- PyTorch NCCL **flight recorder**: `TORCH_NCCL_TRACE_BUFFER_SIZE=2000` and `TORCH_NCCL_DUMP_ON_TIMEOUT=1` dump the last collectives on each rank at timeout; the rank that never entered a collective is the culprit.
- External watchdog: alert if global step hasn't advanced in N minutes.

## Dashboard and alerts
Panels: global tokens/s, MFU, loss, grad norm, per-rank step-time heatmap, GPU SM-active per node, data-loader wait time, checkpoint duration. Page on: step stall, MFU drop > 20% sustained, loss NaN, repeated restarts.

## Verify
- [ ] MFU computed and logged with the formula and peak value documented.
- [ ] Per-rank step time visible; a deliberately throttled GPU shows up as a straggler.
- [ ] Collective timeout and flight recorder enabled; stall alert fires.
