---
id: computing-software.ai-ml-engineering.pytorch.cuda-streams-and-synchronization
name: cuda-streams-and-synchronization
category: computing-software
field: ai-ml-engineering
product: pytorch
tags: [pytorch, cuda-streams, cuda-synchronize, async-execution, non-blocking, pinned-memory, cuda-semantics]
level: practitioner
status: docs-checked
description: "Reason about PyTorch asynchronous CUDA execution: non_blocking copies with pinned memory, side streams with wait_stream and record_stream, events and CUDA_LAUNCH_BLOCKING."
sources:
  - https://github.com/pytorch/pytorch/blob/main/docs/source/notes/cuda.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CUDA streams and synchronization

GPU operations are enqueued and the Python call returns before they finish. Timing, error locations and memory reuse all depend on that.

## What PyTorch synchronises for you
Each device runs operations in queue order, and PyTorch synchronises automatically when copying between CPU and GPU or between GPUs (while the current stream is the default stream). Functions such as `Tensor.to` and `Tensor.copy_` take `non_blocking` to skip that synchronisation when it is unnecessary.

## Overlap host-to-device copies
Host-to-GPU copies are faster from pinned (page-locked) memory. Use `tensor.pin_memory()` or `pin_memory=True` on a DataLoader, then copy with `non_blocking=True`:
```python
loader = DataLoader(ds, pin_memory=True)
for x, y in loader:
    x = x.to("cuda", non_blocking=True)
    y = y.to("cuda", non_blocking=True)
```
The CUDA notes warn that overusing pinned memory can seriously hurt system performance.

## Side streams
Operations inside one stream run in creation order; different streams can run concurrently unless you synchronise. With non-default streams synchronisation is your responsibility.
```python
s = torch.cuda.Stream()
s.wait_stream(torch.cuda.default_stream(cuda))    # inputs produced on the default stream
with torch.cuda.stream(s):
    B = torch.sum(A)
A.record_stream(s)                                # do not free A before the side stream finishes with it
torch.cuda.default_stream(cuda).wait_stream(s)    # before consuming B on the default stream
```
- Without `wait_stream`, the side stream may start before the input is ready, with no error.
- `wait_stream` is needed even without a read dependency (for example writing into a tensor on a side stream).
- Waiting immediately after launching on `s` defeats the point, since it prevents parallel work.

## Events and timing
```python
start, end = torch.cuda.Event(enable_timing=True), torch.cuda.Event(enable_timing=True)
start.record(); out = model(x); end.record()
torch.cuda.synchronize()          # wait for the events to be recorded
print(start.elapsed_time(end), "ms")
```
Timing without synchronisation is not accurate.

## Debugging async errors
An error on the GPU is not reported until the operation actually executes, so the stack trace does not show where it was requested. Set `CUDA_LAUNCH_BLOCKING=1` to force synchronous execution while debugging.

## Checked
2026-11-01. Confirmed in the PyTorch CUDA semantics notes (docs/source/notes/cuda.md): asynchronous execution, automatic copy synchronisation, non_blocking, CUDA_LAUNCH_BLOCKING, Event timing example, stream semantics, wait_stream and record_stream example, pinned memory and pin_memory=True advice. Removed (not confirmed in fetched sources): list of hidden sync ops, set_sync_debug_mode, device-to-host non_blocking caveat, allocator explanation beyond the notes, profiler check, num_workers value.
Method: documentation only; no commands were run.
