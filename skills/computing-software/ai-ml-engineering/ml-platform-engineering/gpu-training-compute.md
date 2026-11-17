---
id: computing-software.ai-ml-engineering.ml-platform-engineering.gpu-training-compute
name: gpu-training-compute
category: computing-software
field: ai-ml-engineering
product: ml-platform-engineering
tags: [gpu, gpu-memory, training-compute, mixed-precision, adam-optimizer-state, activation-checkpointing, fsdp, zero, kubernetes, nvidia-device-plugin, gpu-operator, slurm, sbatch, gres, nccl, mig, multi-instance-gpu, resource-quotas, dcgm, dcgm-exporter, nvidia-smi, gpu-utilization, preemption, spot-instances, checkpointing, ml-platform]
level: advanced
status: draft
description: "Size GPU training jobs (~16-20 bytes/param for Adam mixed precision), schedule on Kubernetes or Slurm, tune NCCL, use MIG and quotas, monitor with DCGM, checkpoint for preemption."
sources:
  - https://docs.nvidia.com/datacenter/tesla/mig-user-guide/
  - https://docs.nvidia.com/datacenter/dcgm/latest/index.html
  - https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/index.html
  - https://kubernetes.io/docs/tasks/manage-gpus/scheduling-gpus/
  - https://slurm.schedmd.com/documentation.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# GPU Training Compute — size it, schedule it, keep it busy, survive preemption

**Goal:** know before launch whether a job fits, request the right GPUs from the scheduler, confirm they are actually used, and lose minutes, not days, when a node disappears.

## 1. Memory math before you request hardware
Full training with Adam in mixed precision needs per parameter roughly:
| Item | Bytes |
|---|---|
| bf16/fp16 weights | 2 |
| bf16/fp16 gradients | 2 |
| fp32 master weights | 4 |
| Adam first + second moments (fp32) | 8 |
| **Total (states only)** | **~16** |
Budget **16–20 bytes/param** to cover fragmentation, buffers and framework overhead, **plus activations**, which scale with batch × sequence length × hidden size × layers and can exceed the states. Examples: 1B params ≈ 16–20 GB of states; 7B ≈ 112–140 GB — more than one 80 GB GPU before a single activation, so it needs sharding.
Levers, roughly in order of cost:
- Activation (gradient) checkpointing: recompute in backward, ~20–30% slower, large activation savings.
- Smaller micro-batch plus gradient accumulation.
- Shard states across GPUs: PyTorch FSDP or DeepSpeed ZeRO stage 1/2/3 divide optimizer/gradient/weight memory by the number of GPUs.
- LoRA/QLoRA: train adapters only; frozen base in bf16 (2 bytes/param) or 4-bit (~0.5) — see computing-software.ai-ml-engineering.hugging-face.fine-tuning-with-trainer.

## 2. Scheduling on Kubernetes
- Install the NVIDIA GPU Operator (or device plugin); pods request `resources.limits: {nvidia.com/gpu: 4}`. GPUs are whole integers and cannot be overcommitted.
- Use node affinity on GPU-type labels and taints to keep CPU pods off GPU nodes.
- Multi-node jobs need gang scheduling (all pods start together or none): Kubeflow Training Operator, Volcano or Kueue.
- Kueue or namespace `ResourceQuota` on `requests.nvidia.com/gpu` give teams fair shares and queueing instead of first-come grabbing.
- Shared memory: PyTorch DataLoader workers need more than the default 64 MB `/dev/shm`; mount an `emptyDir` with `medium: Memory`.

## 3. Scheduling on Slurm
```bash
#SBATCH --nodes=2 --ntasks-per-node=1 --gpus-per-node=8 --cpus-per-task=64
#SBATCH --time=24:00:00 --requeue --signal=B:USR1@300
srun torchrun --nnodes=2 --nproc_per_node=8 --rdzv_backend=c10d \
  --rdzv_endpoint=$(scontrol show hostnames $SLURM_NODELIST | head -n1):29500 train.py
```
`--gres=gpu:8` is the older equivalent of `--gpus-per-node`. Fairshare, QOS and partition limits implement quotas.

## 4. NCCL and the interconnect
- Multi-node throughput depends on InfiniBand/RoCE or fast Ethernet (EFA on AWS). `NCCL_DEBUG=INFO` prints which transport was chosen — if it says `NET/Socket` on an IB cluster, you are on the slow path.
- `NCCL_SOCKET_IFNAME` selects the right network interface when nodes have several.
- Hangs at startup are usually firewall/port issues or mismatched NCCL/driver versions; a hang mid-training is often one rank crashing or a collective called in a different order on different ranks. `TORCH_NCCL_ASYNC_ERROR_HANDLING=1` (default in recent PyTorch) turns hangs into errors — check your version's variable name.
- Benchmark with `nccl-tests` (`all_reduce_perf`) before blaming the model.

## 5. MIG and sharing
Multi-Instance GPU (A100, H100 and later) partitions one GPU into up to 7 isolated instances with dedicated memory and compute (profiles such as `1g.10gb`, `3g.40gb` on 80 GB cards). Good for notebooks, small fine-tunes and inference; useless for large training, which wants whole GPUs. MIG layouts are set per node by an admin and exposed to Kubernetes as resources like `nvidia.com/mig-1g.10gb`.

## 6. Monitor real utilisation
- Quick look: `nvidia-smi`, `nvidia-smi dmon`, or `nvidia-smi --query-gpu=utilization.gpu,memory.used,power.draw --format=csv -l 5`.
- Fleet: DCGM Exporter to Prometheus/Grafana. Gotcha: `DCGM_FI_DEV_GPU_UTIL` (same as nvidia-smi "utilization") only means *a kernel was running*; it can read 100% while the SMs are mostly idle. Use `DCGM_FI_PROF_SM_ACTIVE` / `DCGM_FI_PROF_PIPE_TENSOR_ACTIVE` and tokens- or samples-per-second (MFU) to judge efficiency.
- Low utilisation usually means data loading, small batches or synchronous checkpointing — profile before buying GPUs. Alert on jobs idling GPUs for >30 minutes.

## 7. Checkpointing for preemption
- Save full state (model, optimizer, scheduler, step, RNG, data-loader position) every 15–60 minutes of compute, written atomically to shared or object storage — see computing-software.ai-ml-engineering.pytorch.training-loop.
- Catch the termination signal (SIGTERM on Kubernetes, the `--signal` from Slurm) and write a final checkpoint. Kubernetes' default grace period is 30 s; raise `terminationGracePeriodSeconds` if saving takes longer. Cloud spot notices are short (about 2 minutes on AWS, about 30 s on GCP — check current docs).
- On start, always auto-resume from the latest valid checkpoint; keep the last 2–3 in case the newest is corrupt.
- For very large models use sharded/async saves (PyTorch Distributed Checkpoint).

## Verify
- [ ] A memory estimate (states + activations) exists for the job and matches observed peak within ~20%.
- [ ] GPU requests, node selection and team quota are declared in the job spec.
- [ ] `NCCL_DEBUG=INFO` shows the high-speed transport on multi-node jobs; `all_reduce_perf` meets expected bandwidth.
- [ ] Dashboards show SM activity and throughput, not only GPU-util percent.
- [ ] Killing a node mid-run leads to automatic resume from a checkpoint less than an hour old.
