---
id: computing-software.computer-graphics-engineering.directx.d3d12-work-graphs
name: d3d12-work-graphs
category: computing-software
field: computer-graphics-engineering
product: directx
tags: [computer-graphics-engineering, directx, d3d12-advanced-features, work-graphs, gpu-driven-rendering, gpu-work-creation]
level: sme
status: docs-checked
description: "Build D3D12 work graphs (node shaders, records, backing memory, DispatchGraph) so the GPU schedules its own work without ExecuteIndirect round trips."
sources: ["https://github.com/microsoft/DirectX-Specs/blob/master/d3d/WorkGraphs.md", "https://learn.microsoft.com/en-us/windows/win32/direct3d12/d3d12-work-graphs"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# D3D12 work graphs

**Goal:** express GPU-generated work as a graph of shader nodes that emit records to each other,
scheduled by the GPU (Shader Model 6.8, `D3D12_WORK_GRAPHS_TIER_1_0`).

## 1. Nodes
```hlsl
struct Tile { uint2 xy; };
[Shader("node")] [NodeLaunch("broadcasting")] [NodeDispatchGrid(64,64,1)] [NumThreads(8,8,1)]
void Classify(uint2 tid : SV_DispatchThreadID,
              [MaxRecords(1)] NodeOutput<Tile> Shade)
{
    bool hit = NeedsShading(tid);
    ThreadNodeOutputRecords<Tile> r = Shade.GetThreadNodeOutputRecords(hit ? 1 : 0);
    if (hit) r.Get().xy = tid;
    r.OutputComplete();
}
[Shader("node")] [NodeLaunch("thread")]
void Shade(ThreadNodeInputRecord<Tile> t) { ShadeTile(t.Get().xy); }
```
Launch modes: broadcasting (grid per record), coalescing (batch records into a group),
thread (one thread per record).

## 2. Host side
1. State object with a work-graph subobject (`CD3DX12_WORK_GRAPH_SUBOBJECT`), entry node named.
2. `GetWorkGraphMemoryRequirements` then allocate backing memory (a buffer you provide; it must be at least
   `MinSizeInBytes`, sizes beyond `MaxSizeInBytes` are wasted, and a min of 0 means `null` is allowed).
3. `SetProgram` with `D3D12_PROGRAM_TYPE_WORK_GRAPH` and `D3D12_SET_WORK_GRAPH_FLAG_INITIALIZE`
   on first use of the backing memory.
4. `DispatchGraph` with CPU or GPU input records.

## 3. When to use
- Classify-then-shade, GPU culling cascades, variable work expansion: anything that today
  needs ExecuteIndirect plus counter buffers plus barriers.
- Mesh nodes feed mesh shaders from the graph, but need `D3D12_WORK_GRAPHS_TIER_1_1`, which the spec describes as a preview phase
  not supported by all drivers, with no capability bit to check.

## Gotchas
- Output record limits (`MaxRecords`) are hard caps; exceeding them is undefined behaviour.
- A node that outputs to itself must declare `NodeMaxRecursionDepth`; the graph is otherwise acyclic with a depth limit of 32 including recursion.
- Check `D3D12_FEATURE_D3D12_OPTIONS21` `WorkGraphsTier` before use and keep an ExecuteIndirect fallback.
- Backing memory must not be used by command lists running in parallel on multiple queues.

## Verify
- [ ] Graph output matches the ExecuteIndirect path image-for-image.
- [ ] GPU timing shows no idle gaps between classify and shade phases.

## Checked

Checked 2026-10-26 against the DirectX-Specs D3D12 Work Graphs spec (v1.012, 2026-02-04; repository current to 2026-10-22). Confirmed: D3D12_WORK_GRAPHS_TIER_1_0, SM 6.8 requirement for node shaders, [NodeDispatchGrid], [MaxRecords] undefined-behaviour rule, NodeMaxRecursionDepth requirement and depth limit 32, GetThreadNodeOutputRecords, ThreadNodeInputRecord with Get(), GetWorkGraphMemoryRequirements fields, D3D12_SET_WORK_GRAPH_FLAG_INITIALIZE, D3D12_PROGRAM_TYPE_WORK_GRAPH, DispatchGraph with CPU or GPU records. Corrected: mesh nodes are tied to Tier 1.1 and still described as preview. WorkGraphsTier is in D3D12_FEATURE_D3D12_OPTIONS21. Removed: 'larger is faster' and Agility SDK/PIX version advice.
Method: documentation only; no commands were run.
