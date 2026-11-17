---
id: computing-software.ai-ml-engineering.vllm.expert-parallel-deployment
name: expert-parallel-deployment
category: computing-software
field: ai-ml-engineering
product: vllm
tags: [expert-parallel, enable-expert-parallel, all2all-backend, deepep, moe]
level: advanced
status: docs-checked
description: "Serve Mixture-of-Experts models with --enable-expert-parallel and choose an --all2all-backend."
sources:
  - https://docs.vllm.ai/en/latest/serving/expert_parallel_deployment/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: place MoE experts on separate GPUs for better locality and throughput.

Prerequisites: install DeepEP (vLLM's EP kernels guide), the DeepGEMM library, and for disaggregated serving `gdrcopy` via `install_gdrcopy.sh`. On CUDA 13+, the `deepep_v2` backend needs NCCL 2.30.4 or newer.

Enable with `--enable-expert-parallel`. The size is computed: `EP_SIZE = TP_SIZE x DP_SIZE`. Expert layers are sharded across all EP ranks; attention layers are replicated across DP ranks when `TP = 1` and sharded by tensor parallelism inside each DP group when `TP > 1`. Without the flag MoE layers use a tensor parallel group of size `TP x DP`.

```bash
vllm serve deepseek-ai/DeepSeek-V3-0324 \
  --tensor-parallel-size 1 --data-parallel-size 8 --enable-expert-parallel
```

This fits an 8-GPU H200 (or H20) node; for H100 use a smaller model or multi-node.

Backends via `--all2all-backend`:
- `allgather_reducescatter`: default, any EP+DP setup.
- `deepep_high_throughput`: multi-node prefill.
- `deepep_low_latency`: multi-node decode, CUDA graphs.
- `flashinfer_nvlink_one_sided` / `flashinfer_nvlink_two_sided`: multi-node NVLink systems.
- `mori`: ROCm (AMD Instinct).
- `passthrough` is internal and not accepted on the CLI.

MoRI on ROCm: `VLLM_MORI_EP_V2` unset uses EPv2 with fallback to EPv1; `1` forces EPv2; `0` forces EPv1. Across nodes EPv1 uses InterNodeV1LL when `--max-num-batched-tokens` is at most `VLLM_MORI_DISPATCH_INTER_KERNEL_SWITCH_THRESHOLD` (default 256).

## Checked

2026-11-03. Confirmed against the Expert Parallel Deployment page (docs.vllm.ai/en/latest/): prerequisites, EP size formula, layer behaviour, backend table and MoRI EP version switch.

Method: documentation only; no commands were run.
