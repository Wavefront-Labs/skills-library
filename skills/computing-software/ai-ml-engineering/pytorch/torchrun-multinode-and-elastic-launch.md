---
id: computing-software.ai-ml-engineering.pytorch.torchrun-multinode-and-elastic-launch
name: torchrun-multinode-and-elastic-launch
category: computing-software
field: ai-ml-engineering
product: pytorch
tags: [pytorch, torchrun-multinode, elastic-training, torchrun, rendezvous, c10d]
level: practitioner
status: gated
description: "Launch multi-node PyTorch jobs with torchrun: rendezvous backends, environment variables, elastic restarts, SLURM integration and common connection failures."
sources:
  - https://pytorch.org/docs/stable/elastic/run.html
  - https://pytorch.org/docs/stable/elastic/rendezvous.html
  - https://pytorch.org/tutorials/intermediate/ddp_series_multinode.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# torchrun multi-node and elastic launch

Checked against torch 2.14's `python -m torch.distributed.run --help` and source (`local_elastic_agent.py`). No multi-node cluster, GPU, NCCL or SLURM exists here, so the launch commands could not be executed (gated: unconfirmed, source is paywalled or blocked). On the Windows CPU wheel even `--standalone` and `--rdzv_backend=static` fail with `use_libuv was requested but PyTorch was built without libuv support` (setting `USE_LIBUV=0` did not help the launcher), so the worker tests for these skills used `mp.spawn` instead.

## Single node
```bash
torchrun --standalone --nproc_per_node=8 train.py --cfg cfg.yaml
```

## Multi-node (run on every node)
```bash
torchrun --nnodes=4 --nproc_per_node=8 \
  --rdzv_backend=c10d --rdzv_endpoint=$HEAD_NODE:29500 --rdzv_id=$JOB_ID \
  train.py
```
In the script:
```python
dist.init_process_group("nccl")                        # reads env vars set by torchrun
local_rank = int(os.environ["LOCAL_RANK"]); torch.cuda.set_device(local_rank)
rank, world = dist.get_rank(), dist.get_world_size()
```
Env vars the agent sets for each worker (read in `local_elastic_agent.py`): `RANK`, `GROUP_RANK`, `ROLE_RANK`, `ROLE_NAME`, `LOCAL_RANK`, `WORLD_SIZE`, `LOCAL_WORLD_SIZE`, `GROUP_WORLD_SIZE`, `ROLE_WORLD_SIZE`, `MASTER_ADDR`, `MASTER_PORT`, `TORCHELASTIC_RESTART_COUNT`, `TORCHELASTIC_MAX_RESTARTS`, `TORCHELASTIC_RUN_ID`. `TORCHELASTIC_ERROR_FILE` is a separate variable read by `@record`. Use `LOCAL_RANK` for device selection, never `RANK`.

## SLURM
```bash
#SBATCH --nodes=4 --ntasks-per-node=1 --gpus-per-node=8
head=$(scontrol show hostnames $SLURM_JOB_NODELIST | head -n1)
srun torchrun --nnodes=$SLURM_NNODES --nproc_per_node=8 \
  --rdzv_backend=c10d --rdzv_endpoint=$head:29500 --rdzv_id=$SLURM_JOB_ID train.py
```
One srun task per node; torchrun spawns the 8 local workers.

## Elastic and fault tolerance
- `--max_restarts=3` (help text: "Maximum number of worker group restarts before failing"; underscore and hyphen spellings are both accepted): if any worker fails, all workers are stopped and restarted from scratch; your script must resume from the latest checkpoint on start (restart behaviour not run).
- `--nnodes=2:4` (help: "the range of nodes in form <minimum_nodes>:<maximum_nodes>"): elastic range; training continues if nodes leave or join, with re-rendezvous. Your code must handle a changing world size (re-shard data, rescale batch/LR or keep global batch fixed by changing accumulation).
- Checkpoint often enough that a restart loses minutes, not hours.

## Common failures
- Hang at `init_process_group`: nodes can't reach `rdzv_endpoint` (firewall, wrong interface). Test `nc -zv head 29500` (not run). Set `NCCL_SOCKET_IFNAME=eth0` / `GLOO_SOCKET_IFNAME` to the right interface.
- "Address already in use": stale process or two jobs on one port; change `--rdzv_endpoint` port.
- Mismatched `--nproc_per_node` or code versions across nodes: hangs at first collective. Ship the same container to all nodes.
- Only rank 0 should write logs/checkpoints: guard with `if rank == 0`.
- Exceptions on one rank leave others blocked in a collective until timeout; torchrun's error file (`TORCHELASTIC_ERROR_FILE`) plus `@record` from `torch.distributed.elastic.multiprocessing.errors` surface the root cause (`from torch.distributed.elastic.multiprocessing.errors import record` imports on 2.14).

## Verify
Smoke test: a script that all-reduces `torch.ones(1)` and prints `rank, world, result` on every rank; result must equal world size.
