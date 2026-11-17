---
id: computing-software.computer-graphics-engineering.gpu-optimisation.delta-colour-compression-dcc
name: delta-colour-compression-dcc
category: computing-software
field: computer-graphics-engineering
product: gpu-optimisation
tags: [computer-graphics-engineering, gpu-optimisation, gpu-memory-bandwidth, dcc, delta-color-compression, render-target-compression, fast-clear, amd-rdna, bandwidth]
level: advanced
status: draft
description: "Keep render targets compressed with delta colour compression (DCC) and depth compression: what disables it (UAV writes, formats, aliasing), fast clears, and decompression costs."
sources: ["https://gpuopen.com/learn/dcc-overview/", "https://gpuopen.com/learn/rdna-performance-guide/", "https://developer.nvidia.com/blog/advanced-api-performance-memory-and-resources/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Delta colour compression (DCC)

## 1. What it is
Lossless compression of render targets in blocks (AMD DCC, NVIDIA's equivalent, depth HTILE /
Z-compression). Pixels in a block are stored as a base value plus small deltas; smooth content
compresses well, cutting bandwidth for writes, blending and later texture reads (when the texture
unit can read compressed data directly, as on GCN4+/RDNA).

## 2. What keeps it enabled
- Render target usage (`ALLOW_RENDER_TARGET` / `COLOR_ATTACHMENT`) with optimal tiling.
- Supported formats (most colour formats; some like certain 96-bit formats don't).
- Clearing with **fast clears** to supported clear colours (RDNA: specific values like 0/1 for
  channels allow "clear-to-constant" without writing memory). Use the same clear value at resource
  creation (`D3D12_CLEAR_VALUE`) and clear time.

## 3. What disables or decompresses
- **UAV/storage writes** to the resource: historically disabled DCC on AMD (RDNA2+ supports
  compressed UAV writes for many cases); avoid `ALLOW_UNORDERED_ACCESS` on render targets unless
  needed.
- Transitions to states where the consumer can't read compressed data (e.g. copy to non-
  compressible, some shader resource reads on older GPUs) trigger a **decompression** pass (visible
  as extra GPU work in RGP barriers view).
- Aliasing a DCC surface with another resource, mutable format views with incompatible formats.
- Partial clears or clears with non-fast values.

## 4. Practical rules (AMD RDNA guide)
- Create render targets with only needed flags.
- Use fast-clear-friendly clear colours (0,0,0,0 / 1,1,1,1).
- Check barriers in RGP: "DCC decompress", "FMask decompress", "Init/clear" events with their cost.
- Depth: keep HiZ/HTILE valid; avoid writing depth from compute (UAV on depth isn't possible anyway)
  and avoid frequently switching depth comparison direction.

## Gotchas
- Noisy content (film grain, dithering) compresses poorly; apply noise in the last pass.
- Copying compressed resources may force decompression; prefer rendering directly into the final
  target.

## Verify
- [ ] RGP shows no unexpected decompress barriers per frame.
- [ ] Bandwidth counters drop when flags are corrected.
