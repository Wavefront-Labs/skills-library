---
id: computing-software.ai-ml-engineering.pytorch.collective-ops-and-process-groups
name: collective-ops-and-process-groups
category: computing-software
field: ai-ml-engineering
product: pytorch
tags: [pytorch, collective-ops, process-groups, all-reduce, all-gather, torch-distributed, nccl, device-mesh]
level: practitioner
status: gated
description: "Use torch.distributed collectives correctly: init_process_group, all_reduce/all_gather/reduce_scatter/broadcast, subgroups, DeviceMesh and rules that avoid hangs."
sources:
  - https://pytorch.org/docs/stable/distributed.html
  - https://pytorch.org/tutorials/intermediate/dist_tuto.html
  - https://pytorch.org/tutorials/recipes/distributed_device_mesh.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Collective ops and process groups

**Goal:** write custom distributed logic (metric aggregation, gathering predictions, custom parallelism) without deadlocks.

## Setup
```python
import os, torch, torch.distributed as dist
dist.init_process_group(backend="nccl")              # torchrun sets RANK, WORLD_SIZE, MASTER_ADDR (nccl needs CUDA; not run)
local_rank = int(os.environ["LOCAL_RANK"]); torch.cuda.set_device(local_rank)
rank, world = dist.get_rank(), dist.get_world_size()
...
dist.destroy_process_group()
```
Backends: `nccl` for CUDA tensors, `gloo` for CPU tensors (can create both: `backend="cuda:nccl,cpu:gloo"`). On the Windows CPU wheel `dist.is_nccl_available()` is False and that combined string raises `Distributed package doesn't have NCCL built in`; every collective below was run with `gloo` on 2 CPU processes (`mp.spawn` with a file init method, because `torchrun` fails on this wheel; see the torchrun skill). The `nccl` and CUDA lines were not run (gated: unconfirmed, source is paywalled or blocked).

## Core collectives
| Op | Use |
|---|---|
| `all_reduce(t, op=ReduceOp.SUM)` | sum metrics/grads in place on every rank |
| `all_gather_into_tensor(out, t)` | concatenate equal-size tensors from all ranks |
| `all_gather_object(list, obj)` | arbitrary picklable objects (slow; small data only) |
| `reduce_scatter_tensor(out, t)` | sum then shard (FSDP building block) |
| `broadcast(t, src=0)` | send rank-0 value to all (seeds, configs) |
| `barrier()` | sync point; avoid in hot loops |

Measured on 2 ranks: `all_reduce` of `[rank+1]` gave 3.0; `all_gather_into_tensor` gave `[0,0,1,1]`; `all_gather_object` returned both dicts; `reduce_scatter_tensor` of `arange(4)+rank` gave `[1,3]` on rank 0; `broadcast` from 0 gave 42; `async_op=True` returned a `Work` whose `wait()` returned True.
Example: global accuracy
```python
stats = torch.tensor([correct, total], device="cuda", dtype=torch.float64)   # "cpu" with gloo
dist.all_reduce(stats)
acc = (stats[0] / stats[1]).item()
```
Unequal sizes for all_gather: gather lengths first, pad to max, gather, then trim.

## Subgroups and meshes
```python
from torch.distributed.device_mesh import init_device_mesh
mesh = init_device_mesh("cuda", (2, 4), mesh_dim_names=("dp", "tp"))   # "cpu" with a 1-D mesh worked: get_group("dp") returned a ProcessGroup
tp_group = mesh.get_group("tp")
dist.all_reduce(t, group=tp_group)
```
`dist.new_group(ranks)` must be called by **all** ranks, with the same arguments and in the same order, even ranks not in the group (called by both ranks with `[0]` it returned a `ProcessGroup`; the failure mode if skipped was not tried).

## Async
`work = dist.all_reduce(t, async_op=True)`; do other work; `work.wait()` before reading `t`.

## Rules that prevent hangs
- Every rank must call the same collectives in the same order with matching shapes and dtypes. A collective inside `if rank == 0:` hangs everyone else: with a 6 s timeout on gloo, rank 0 alone in `all_reduce` ended with the process terminating (exit code 3221226505, 0xC0000409) rather than a catchable Python exception. A shape mismatch (2 vs 3 elements) did not error immediately either: rank 0 returned and rank 1 got `RuntimeError: ... Timed out waiting 6000ms for send operation`.
- Data-dependent early exits (one rank runs out of data) desync ranks; use `drop_last=True`/equal shards or join contexts.
- Set a timeout: `init_process_group(timeout=datetime.timedelta(minutes=10))` (the argument was accepted and enforced on gloo; see above); debug with `TORCH_DISTRIBUTED_DEBUG=DETAIL` and `NCCL_DEBUG=INFO` (not run).

## Verify
- [ ] Test with `torchrun --nproc_per_node=2` on CPU using `gloo` in CI (on Linux; on this Windows wheel `torchrun` failed with `use_libuv was requested but PyTorch was built without libuv support`).
- [ ] Aggregated metric equals the single-process metric on the same data.
