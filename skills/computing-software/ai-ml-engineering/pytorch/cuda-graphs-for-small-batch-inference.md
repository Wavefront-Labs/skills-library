---
id: computing-software.ai-ml-engineering.pytorch.cuda-graphs-for-small-batch-inference
name: cuda-graphs-for-small-batch-inference
category: computing-software
field: ai-ml-engineering
product: pytorch
tags: [pytorch, cuda-graphs, cudagraph, reduce-overhead, inference-latency, static-shapes]
level: practitioner
status: docs-checked
description: "Cut PyTorch launch overhead with CUDA graphs via torch.compile reduce-overhead or manual torch.cuda.graph capture, with static buffers and shape bucketing."
sources:
  - https://pytorch.org/docs/stable/notes/cuda.html#cuda-graphs
  - https://pytorch.org/blog/accelerating-pytorch-with-cuda-graphs/
  - https://pytorch.org/docs/stable/torch.compiler_cudagraph_trees.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CUDA graphs for small-batch inference

At small batch sizes the GPU often waits on Python, dispatch and kernel launches. A CUDA graph records the kernel sequence once and replays it with a single launch (`cudaGraphLaunch`), skipping argument setup and dispatch layers. The CUDA notes say to try it when all or part of the network is graph-safe (static shapes, static control flow) and runtime is at least somewhat CPU-limited. Measure your own speed-up.

## Easiest: torch.compile
```python
model = torch.compile(model, mode="reduce-overhead")
```
CUDA graph trees re-record a graph for every unique input shape. Outputs live in graph-managed memory and a later run can overwrite them (accessing an overwritten output raises a RuntimeError): `out = model(x).clone()` if you keep it across calls, or call `torch.compiler.cudagraph_mark_step_begin()` between steps.

## Manual capture
```python
static_x = torch.zeros(8, 512, device="cuda")
s = torch.cuda.Stream(); s.wait_stream(torch.cuda.current_stream())
with torch.cuda.stream(s):
    for _ in range(3): model(static_x)                # warm up on a side stream
torch.cuda.current_stream().wait_stream(s)
g = torch.cuda.CUDAGraph()
with torch.inference_mode(), torch.cuda.graph(g):
    static_y = model(static_x)
def run(x):
    static_x.copy_(x)                                 # write into the captured input buffer
    g.replay()
    return static_y.clone()
```
Or `torch.cuda.make_graphed_callables(module, (sample_input,))` for partial-network capture: it graphs forward and backward separately, is autograd-aware and handles warmup and static buffers for you.

## Constraints (from the CUDA notes)
- **Static shapes and addresses**: every replay uses the same memory addresses, so copy new data into the captured input tensors; dynamic shapes are prohibited. For varying batch sizes, pad to a few fixed sizes and capture one graph per size (the cudagraph-trees doc suggests padding to a few fixed shapes, since each re-recording costs device memory).
- **No CPU sync inside capture**: ops such as `.item()` are prohibited; dynamic control flow based on CPU or GPU data is prohibited (GPU-data-dependent flow only via `torch.cond`).
- **CPU work is not captured**: it is elided during replay.
- **Memory**: captures allocate from a graph-private pool, one per capture by default. `torch.cuda.graph(g2, pool=g1.pool())` lets graphs share a pool, but only if they are always replayed in the order they were captured and never concurrently, so it does not suit independently chosen size buckets.
- Only one capture at a time per process, and no non-captured CUDA work in any thread during capture.
- The CUDA graph API is marked beta and may change.
- Not worth it when GPU time dominates; measure first.

## Verify
Profile one request eagerly and with graphs: the eager trace shows many short kernels separated by gaps; the graph trace shows a dense block. Compare outputs with `torch.testing.assert_close`.

## Checked
2026-11-01. Confirmed in the PyTorch CUDA semantics notes (docs/source/notes/cuda.md, CUDA Graphs section) and the CUDA graph trees page (docs/source/user_guide/torch_compiler/torch.compiler_cudagraph_trees.md): single-launch replay, side-stream warmup, static input copy, `make_graphed_callables`, constraints, private pools and `pool=g1.pool()` ordering rule, `mode="reduce-overhead"`, re-recording per unique shape, output overwrite and clone.
Removed: per-launch microsecond and speed-up multiples, the vLLM/SGLang claim, the cuBLAS handle remark, the dropout/RNG bullet, and the exact error message text.
Method: documentation only; no commands were run.
