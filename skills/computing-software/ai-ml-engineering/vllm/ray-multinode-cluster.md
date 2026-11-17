---
id: computing-software.ai-ml-engineering.vllm.ray-multinode-cluster
name: ray-multinode-cluster
category: computing-software
field: ai-ml-engineering
product: vllm
tags: [ray, multi-node, run-cluster, vllm-host-ip, kuberay]
level: advanced
status: docs-checked
description: "Start a multi-node Ray cluster in containers with run_cluster.sh, including the per-node VLLM_HOST_IP rule."
sources:
  - https://docs.vllm.ai/en/latest/serving/parallelism_scaling/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: run one vLLM model replica across several nodes using Ray.

Requirements: every node needs an identical execution environment (model path and Python packages); containers are recommended. Ray is optional, install with `pip install ray`.

The helper script `examples/ray_serving/run_cluster.sh` starts containers and initializes Ray. By default Docker runs without admin privileges, which blocks GPU performance counters for profiling or tracing; add `--cap-add=CAP_SYS_ADMIN` to enable them.

Head node:

```bash
bash run_cluster.sh vllm/vllm-openai <HEAD_NODE_IP> --head \
  /path/to/huggingface-dir -e VLLM_HOST_IP=<HEAD_NODE_IP>
```

Each worker node:

```bash
bash run_cluster.sh vllm/vllm-openai <HEAD_NODE_IP> --worker \
  /path/to/huggingface-dir -e VLLM_HOST_IP=<WORKER_NODE_IP>
```

`VLLM_HOST_IP` is unique per worker. Keep those shells open: closing any terminates the cluster. All nodes must reach each other by IP.

Security warning: set `VLLM_HOST_IP` to an address on a private network segment. Traffic is unencrypted and the endpoints exchange data in a format that can be exploited to execute arbitrary code if an adversary gains network access.

Verify from any node by entering a container and running `ray status` and `ray list nodes` to confirm the expected node and GPU counts. Then launch with tensor parallel size = GPUs per node and pipeline parallel size = node count. KubeRay is an alternative way to set up the Ray cluster.

## Checked

2026-11-03. Confirmed against the Parallelism and Scaling page (docs.vllm.ai/en/latest/): Ray install, run_cluster.sh, CAP_SYS_ADMIN note, security warning, ray status and TP/PP sizing.

Method: documentation only; no commands were run.
