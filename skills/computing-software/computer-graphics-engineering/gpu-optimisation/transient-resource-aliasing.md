---
id: computing-software.computer-graphics-engineering.gpu-optimisation.transient-resource-aliasing
name: transient-resource-aliasing
category: computing-software
field: computer-graphics-engineering
product: gpu-optimisation
tags: [computer-graphics-engineering, gpu-optimisation, gpu-memory-bandwidth, transient-resources, memory-aliasing, placed-resources, render-graph, aliasing-barriers, vram]
level: advanced
status: draft
description: "Save GPU memory by aliasing transient render targets: lifetime analysis, placed resources in shared heaps, aliasing barriers and initialisation rules in D3D12 and Vulkan."
sources: ["https://learn.microsoft.com/en-us/windows/win32/direct3d12/memory-aliasing-and-data-inheritance", "https://docs.vulkan.org/spec/latest/chapters/resources.html#resources-memory-aliasing", "https://gpuopen.com/learn/vulkan-device-memory/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Transient resource aliasing

## 1. Idea
Many render targets live only within part of a frame (G-buffer temporaries, SSAO buffers, bloom
chain, blur scratch). Resources whose lifetimes don't overlap can share the same memory. Frame
graphs compute lifetimes and assign memory offsets automatically; savings of 30-50% of render
target memory are common.

## 2. D3D12
- Create a heap (`CreateHeap`, `D3D12_HEAP_FLAG_ALLOW_ONLY_RT_DS_TEXTURES` on tier 1 hardware,
  or mixed on resource heap tier 2).
- Create **placed resources** at offsets (`CreatePlacedResource`) - multiple resources overlapping
  the same range.
- Before using a resource whose memory was used by another, issue an **aliasing barrier**
  (`D3D12_RESOURCE_BARRIER_TYPE_ALIASING` with before/after resources) and then **initialise** it:
  render targets/depth must be cleared, discarded (`DiscardResource`) or fully copied over before
  other use, because contents are undefined (and compression metadata invalid).

## 3. Vulkan
- Allocate one `VkDeviceMemory` (or VMA allocation) and bind multiple images with
  `vkBindImageMemory` at overlapping offsets (images need compatible memory types; create with
  `VK_IMAGE_CREATE_ALIAS_BIT` only when sharing contents between aliases, not needed for pure
  reuse).
- Synchronise with a barrier from the previous user's last access to the new user's first access,
  with `oldLayout = UNDEFINED` for the new image (discarding contents).
- VMA: allocate with `VMA_ALLOCATION_CREATE_CAN_ALIAS_BIT`-style usage and `vmaBindImageMemory2`
  with offsets.

## 4. Allocation strategy
Sort transient resources by size, assign offsets with an interval-graph colouring (greedy by
lifetime start, reuse free ranges). Keep separate heaps for different resource classes where the
hardware requires (RT/DS vs buffers vs textures on tier 1).

## Gotchas
- Forgetting initialisation after aliasing shows garbage or corrupts compression (DCC/HTILE)
  leading to subtle artefacts; always clear/discard.
- Async compute: lifetimes must consider cross-queue overlap; alias only after synchronisation.
- History resources (TAA, previous depth) live across frames: never transient.

## Verify
- [ ] Memory report shows transient heap size vs sum of individual resources.
- [ ] Debug layer / validation clean; GPU-based validation detects no uninitialised reads.
