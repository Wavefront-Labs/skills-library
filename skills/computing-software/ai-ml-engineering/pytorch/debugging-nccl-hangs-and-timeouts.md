---
id: computing-software.ai-ml-engineering.pytorch.debugging-nccl-hangs-and-timeouts
name: debugging-nccl-hangs-and-timeouts
category: computing-software
field: ai-ml-engineering
product: pytorch
tags: [pytorch, nccl-debug, collective-timeout, flight-recorder, torch-distributed, hang-debugging]
level: practitioner
status: docs-checked
description: "Debug PyTorch distributed hangs and NCCL timeouts: NCCL_DEBUG, TORCH_DISTRIBUTED_DEBUG, the flight recorder buffer, py-spy dumps and the usual mismatched-collective causes."
sources:
  - https://docs.pytorch.org/docs/stable/distributed.html
  - https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/env.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Debugging NCCL hangs and timeouts

Symptom: training freezes, then a watchdog reports a collective operation timeout.

## Turn on diagnostics
```bash
export NCCL_DEBUG=INFO                    # NCCL logging
export NCCL_DEBUG_SUBSYS=INIT,COLL        # narrow output to subsystems
export TORCH_DISTRIBUTED_DEBUG=DETAIL     # consistency/synchronization checks on every collective (slower)
export TORCH_NCCL_TRACE_BUFFER_SIZE=2000  # size of the flight recorder trace buffer
```
`TORCH_DISTRIBUTED_DEBUG` accepts `OFF` (default), `INFO` or `DETAIL`. `DETAIL` surfaces a rank calling a mismatched collective, and can be combined with `TORCH_SHOW_CPP_STACKTRACES=1` for the full call stack. The PyTorch distributed docs also describe a py-spy based dump: `py-spy dump --pid <pid>` (py-spy must be installed and the process needs `SYS_PTRACE`).

## See where each rank is stuck
Run `py-spy dump --pid <pid>` on every rank. One rank elsewhere (data loading, checkpointing) while the others sit in a collective is the cause.

## Usual causes
| Cause | Fix |
|---|---|
| Rank-conditional collective (a barrier or DDP forward on rank 0 only) | every rank must call the same collectives in the same order |
| Uneven data: one rank has more batches | equal shards or drop the last partial batch |
| DDP param unused on some steps | `find_unused_parameters=True` or remove the dead branch |
| Different tensor shapes/dtypes in a collective | make them match; `TORCH_DISTRIBUTED_DEBUG=DETAIL` catches this |
| Rank 0 doing a long checkpoint/eval while others hit the next collective | raise the timeout or checkpoint asynchronously |
| Wrong network interface or RDMA adapter | `NCCL_SOCKET_IFNAME`, `NCCL_IB_HCA` (see the NCCL environment-variable page) |
| GPU fault on one node | check that node's system and driver logs; drain it |
| OOM on one rank killed the process; others wait | check every rank's log, not just rank 0 |

## Verify
After the fix, run with `TORCH_DISTRIBUTED_DEBUG=DETAIL` for a few hundred steps including an eval and a checkpoint; no warnings, no timeouts.

## Checked
2026-11-01. Confirmed against the PyTorch distributed docs source and the NCCL environment-variable page: `NCCL_DEBUG`, `NCCL_DEBUG_SUBSYS`, `NCCL_SOCKET_IFNAME`, `NCCL_IB_HCA`, `TORCH_DISTRIBUTED_DEBUG` levels and `DETAIL` checks, `TORCH_NCCL_TRACE_BUFFER_SIZE`, `find_unused_parameters`, `py-spy dump --pid`. Removed (not confirmed on the pages read): the 10 minute default timeout, `TORCH_NCCL_ASYNC_ERROR_HANDLING`, `TORCH_NCCL_DUMP_ON_TIMEOUT`, the `fr_trace` analyser command, `init_process_group` timeout example, `py-spy dump --native`, `NET/IB` log strings, dmesg/nvidia-smi and nccl-tests commands, the `Join` context.
Method: documentation only; no commands were run.
