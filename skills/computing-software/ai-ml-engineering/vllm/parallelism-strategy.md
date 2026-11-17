---
id: computing-software.ai-ml-engineering.vllm.parallelism-strategy
name: parallelism-strategy
category: computing-software
field: ai-ml-engineering
product: vllm
tags: [parallelism, tensor-parallel-size, pipeline-parallel-size, distributed-executor-backend, kv-cache-size]
level: practitioner
status: docs-checked
description: "Pick tensor and pipeline parallel sizes for a single model replica and read the KV cache log lines."
sources:
  - https://docs.vllm.ai/en/latest/serving/parallelism_scaling/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: choose how to shard one model replica across GPUs and nodes.

Guidelines from the docs:
- Model fits on one GPU: no distributed inference.
- Fits on one node with several GPUs: tensor parallelism, e.g. `tensor_parallel_size=4` on a 4-GPU node.
- Too large for one node: combine tensor and pipeline parallelism. Set `tensor_parallel_size` to GPUs per node and `pipeline_parallel_size` to the number of nodes (e.g. 8 and 2 for two 8-GPU nodes).

Uneven splits: if the model fits in one node but the GPU count does not evenly divide it, use pipeline parallelism with `tensor_parallel_size=1` and `pipeline_parallel_size` equal to the GPU count. Without NVLink (e.g. L40S), pipeline parallelism gives higher throughput and lower communication overhead than tensor parallelism.

After provisioning, start vLLM and read the log:

```text
GPU KV cache size: 643,232 tokens
Maximum concurrency for 40,960 tokens per request: 15.70x
```

The first line is total tokens storable in the GPU KV cache; the second estimates concurrent requests at `ModelConfig.max_model_len` tokens each. If they are below your throughput needs, add GPUs or nodes.

Serving commands:

```bash
vllm serve facebook/opt-13b --tensor-parallel-size 4
vllm serve gpt2 --tensor-parallel-size 4 --pipeline-parallel-size 2   # 8 GPUs
```

Executor backend: Ray for multi-node, native Python `multiprocessing` for single-node. Override with `distributed_executor_backend` (LLM) or `--distributed-executor-backend` (`mp` or `ray`). Ray is an optional dependency (`pip install ray`). MoE models can combine Data Parallel attention with Expert or Tensor Parallel MoE layers (see the Data Parallel Deployment page).

Multi-node:
- Every node needs an identical environment (model path, Python packages); containers are recommended.
- Ray: the repo helper `examples/ray_serving/run_cluster.sh` starts head (`--head`) and worker (`--worker`) containers with a per-node `VLLM_HOST_IP`; verify with `ray status`. Then run one `vllm serve` with `--distributed-executor-backend ray` from any node.
- Multiprocessing: run `vllm serve ... --nnodes 2 --node-rank 0 --master-addr <HEAD_NODE_IP>` on the head and the same with `--node-rank 1` and `--headless` on workers.
- Security: set `VLLM_HOST_IP` to a private network address; traffic is unencrypted and the exchanged data can be exploited for code execution if an adversary reaches the network.
- Fast interconnect matters for tensor parallelism: use InfiniBand and confirm with `NCCL_DEBUG=TRACE` that logs show `NET/IB/GDRDMA`, not `NET/Socket`.

## Checked

Method: 2026-11-08 read the vLLM Parallelism and Scaling page (docs source markdown) in full.
Changes: added the "fits in one node" wording for uneven splits, the multiprocessing and Ray multi-node recipes, the security warning and the NCCL check. Earlier sizing, log-line and backend claims were unchanged and match the page.
