---
id: computing-software.computer-graphics-engineering.opengl.vulkan-execution-and-memory-dependencies
name: vulkan-execution-and-memory-dependencies
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, vulkan, vulkan-synchronization, memory-dependency, availability-visibility, execution-dependency]
level: sme
status: docs-checked
description: "Reason about Vulkan sync like the spec: execution vs memory dependencies, availability and visibility, dependency chains, and choosing stage/access masks."
sources: ["https://github.com/KhronosGroup/Vulkan-Docs/blob/main/chapters/synchronization.adoc", "https://github.com/KhronosGroup/Vulkan-Guide/blob/main/chapters/synchronization.adoc"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Execution and memory dependencies

## Two separate problems
1. **Execution dependency:** operations in the second scope don't *start* (at the given stages)
   until operations in the first scope *finish* (at the given stages). Solves WAR hazards alone.
2. **Memory dependency:** writes from the first scope are made **available** (flushed from
   caches to the memory domain) and then **visible** to the second scope's accesses
   (invalidated from caches). Needed for RAW and WAW hazards.

A barrier = execution dependency (stage masks) + memory dependency (access masks) + optional
layout transition / ownership transfer.

## Choosing masks
- `srcStageMask`: the stages that *wrote* (or read, for WAR). `srcAccessMask`: the **write**
  accesses to make available (a memory dependency makes the first scope's memory writes available).
- `dstStageMask`: the stages that will access next. `dstAccessMask`: the accesses (read or
  write) that must see the data.

| Hazard | Needs |
|---|---|
| Read-after-write (RAW) | full memory dependency |
| Write-after-read (WAR) | execution dependency only (accessMask 0 is fine) |
| Write-after-write (WAW) | memory dependency (writes ordered and visible) |
| Read-after-read | nothing |

## Examples
```text
compute writes SSBO -> vertex shader reads as vertex buffer
  src: COMPUTE_SHADER / SHADER_STORAGE_WRITE   dst: VERTEX_ATTRIBUTE_INPUT / VERTEX_ATTRIBUTE_READ
render to image -> sample in later pass
  src: COLOR_ATTACHMENT_OUTPUT / COLOR_ATTACHMENT_WRITE   dst: FRAGMENT_SHADER / SHADER_SAMPLED_READ
  + layout COLOR_ATTACHMENT_OPTIMAL -> SHADER_READ_ONLY_OPTIMAL
fragment shader samples texture -> transfer overwrites it (WAR)
  src: FRAGMENT_SHADER / 0   dst: COPY / TRANSFER_WRITE
depth write -> next pass depth test
  src: LATE_FRAGMENT_TESTS / DEPTH_STENCIL_ATTACHMENT_WRITE
  dst: EARLY_FRAGMENT_TESTS|LATE_FRAGMENT_TESTS / DEPTH_STENCIL_ATTACHMENT_READ|WRITE
```

## Dependency chains
If barrier A's dst stages intersect barrier B's src stages, A and B chain: work before A
happens-before work after B. This is how a semaphore wait (`COLOR_ATTACHMENT_OUTPUT`) chains
into the layout-transition barrier with srcStage `COLOR_ATTACHMENT_OUTPUT`.

## Layout transitions
A layout transition may perform reads and writes on all memory bound to the image subresource
range; available memory is made visible to it automatically and its writes are made available
automatically. That's why
`oldLayout = UNDEFINED` with srcAccess 0 is valid when you don't care about contents.

## Gotchas
- `ALL_COMMANDS` + `MEMORY_READ|MEMORY_WRITE` always works but serialises the GPU; fine to
  debug a suspected sync bug, never as a final answer.
- Host writes that are available to the host memory domain (coherent memory, or after
  `vkFlushMappedMemoryRanges`) are covered by the host write ordering guarantee of the queue
  submission; no barrier needed.
- Sync2 stage bits split old stages (e.g. `COPY`, `BLIT`, `CLEAR`, `RESOLVE` instead of `TRANSFER`); use them.

## Verify
- [ ] Synchronization validation reports zero hazards; removing any barrier you added produces a reported hazard (proves it is needed).

## Checked

- Date: 2026-10-25. Documentation release: Vulkan specification 1.4.366 (Vulkan-Docs main, commit a8b088a, 2026-10-23), including the generated vk.xml registry.
- Confirmed: Execution dependency alone solves write-after-read; read-after-write and write-after-write need memory dependencies (spec text); a memory dependency makes writes in the first scope available and then visible.
- Confirmed: Dependency chain definition (intersection of second scope of A and first scope of B), layout transition read/write behaviour, and the host write ordering guarantee (queue submission makes host writes available to the host domain visible to the device) were read in the synchronization chapter.
- Confirmed: `COPY`, `BLIT`, `CLEAR`, `RESOLVE` are the synchronization2 split of `TRANSFER` (access mask descriptions).

Method: documentation only; no commands were run.
