---
id: computing-software.ai-ml-engineering.vllm.data-parallel-deployment
name: data-parallel-deployment
category: computing-software
field: ai-ml-engineering
product: vllm
tags: [data-parallel, data-parallel-size, api-server-count, hybrid-lb, external-lb]
level: advanced
status: docs-checked
description: "Run data parallel vLLM with internal, hybrid or external load balancing and multi-node rank flags."
sources:
  - https://docs.vllm.ai/en/latest/serving/data_parallel_deployment/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: replicate model weights across GPUs to serve independent batches in parallel (dense and MoE).

Internal load balancing: one endpoint, `vllm serve $MODEL --data-parallel-size 4 --tensor-parallel-size 2` (8 GPUs). `--max-num-seqs` applies per DP rank, but `--max-num-queued-reqs` and `--max-num-queued-tokens` apply to the whole server; size them near `data-parallel-size * max-num-seqs` plus desired queue depth.

Multi-node (DP=4, two ranks per node):

```bash
# node 0
vllm serve $MODEL --data-parallel-size 4 --data-parallel-size-local 2 \
  --data-parallel-address 10.99.48.128 --data-parallel-rpc-port 13345
# node 1
vllm serve $MODEL --headless --data-parallel-size 4 --data-parallel-size-local 2 \
  --data-parallel-start-rank 2 --data-parallel-address 10.99.48.128 --data-parallel-rpc-port 13345
```

With Ray use `--data-parallel-backend=ray`: one launch command, no address or RPC port needed; set `VLLM_RAY_DP_PACK_STRATEGY="span"` when one DP group spans nodes (then `--data-parallel-size-local` is ignored).

If the API server becomes a bottleneck, add `--api-server-count=4`; it stays confined to the head node.

Hybrid: `--data-parallel-hybrid-lb` makes each node run its own API server for local ranks behind an upstream balancer. Requires `--data-parallel-size-local` and `--data-parallel-start-rank`; incompatible with `--headless`.

External: treat each rank as its own deployment with `--data-parallel-rank N` and its own `--port`; multi-node also needs address and RPC port. `--data-parallel-external-lb` with `--nnodes` infers the rank from `--node-rank` only when `--nnodes` is evenly divisible by `--data-parallel-size`; otherwise set `--data-parallel-rank`.

MoE: expert layers form a `DP x TP` group by default, or EP with `--enable-expert-parallel`.

## Checked

2026-11-03. Confirmed against the Data Parallel Deployment page (docs.vllm.ai/en/latest/): internal, hybrid and external load balancing flags, Ray notes and queue-limit sizing. Fixed the external-LB rank inference rule: it requires --nnodes to be evenly divisible by --data-parallel-size, not merely to divide evenly.

Method: documentation only; no commands were run.
