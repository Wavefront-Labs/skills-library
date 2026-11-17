---
id: computing-software.computer-graphics-engineering.rendering-techniques.virtual-texturing
name: virtual-texturing
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, texturing, virtual-texturing, sparse-virtual-textures, page-table, feedback-buffer, texture-streaming]
level: advanced
status: docs-checked
description: "Design a software virtual texturing system (van Waveren): page table and physical pool, feedback pass, oversubscription LOD bias, LRU replacement."
sources: ["https://mrelusive.com/publications/papers/Software-Virtual-Textures.pdf"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Virtual texturing

Source: J.M.P. van Waveren, "Software Virtual Textures" (id Software). **Goal:** unique
texturing of whole scenes while only a sparse set of pages is resident, with many surfaces sharing
one virtual texture and no per-surface texture selection.

## 1. Components
- **Pages:** the virtual texture is divided into small pages (typically 128 x 128 texels)
  loaded into a pool. The **physical pool** is a fully resident texture logically subdivided
  into such blocks (typically 4096 x 4096 texels, or 1024 pages), while the virtual texture may
  hold on the order of a million pages.
- **Translation:** conceptually walking the mip quad-tree to find the scale and bias that turn a
  virtual address inside a virtual page into a physical address. Variant used in practice: a
  mip-mapped **page table texture** with one texel per virtual page, looked up with a bias that
  accounts for the sizes of the virtual and page-table textures, returning the scale and bias
  (or the best resident coarser page when the desired one is missing). The paper also describes
  a split design (2 bytes per virtual page plus a small mapping texture with one texel per
  physical page, about 2.66 MB total for 1024 x 1024 virtual pages) and computing the mapping
  in the fragment program from the physical page's coordinates and mip.
- **Borders:** pages carry a border for filtering. With a 4-texel inset border on 128 x 128
  pages, 120 x 120 texels of payload remain, about 12 percent overhead. Anisotropic footprints
  stay within one physical page when maximum anisotropy is at most twice the border width. The
  page-table lookup can be biased by the negative base-two log of the maximum anisotropy so the
  anisotropic fetch has the detail it needs (this can cause shimmering if over-applied).

## 2. Feedback rendering
Feedback is rendered to a separate buffer (a separate pass or an additional render target of an
existing pass) storing the virtual page coordinates, desired mip level and virtual texture ID.
Because it is depth tested, invisible pages are not requested. In a separate pass it is fine to
render at a significantly lower resolution (say 10x smaller). Only texture coordinates are used,
never texture data (which may not be resident). The analysis may use frame-old data at one
frame of latency; it condenses the buffer into unique pages (the quad-tree of needed pages) and
sorts by priority: the farther the desired mip is from the resident mip, and the more samples a
page has in the feedback buffer, the higher the priority.

## 3. Oversubscription and replacement
- Track how many resident pages the previous frame's feedback needed: above a high water mark,
  increment the LOD bias used when generating feedback; below a low water mark, decrement it,
  clamped so it never goes negative. The system backs off detail without thrashing and adds it
  back when not strained.
- Replacement: pages sorted by priority; finer mips are replaced first, then by frames since
  last use, so the finest-level pages follow an LRU policy. When the GPU stops using a page it
  drops to the coarser parent page.
- Avoid popping when a finer page arrives: build the physical page of the finer mip by
  upsampling the coarser mip before the coarser one is magnified, rather than letting bilinear
  magnification pop to the finer data.
- Streaming pages are transcoded (JPEG-like or JPEG-XR source to DXT) on parallel jobs.

## Gotchas
- Feedback mip selection must match the hardware's mip and anisotropy behaviour, or the system
  requests too little detail.

## Verify
- [ ] Debug view colours pages by resident mip; no black or garbage pages.
- [ ] Texture memory stays at the pool size regardless of how many unique textures the scene uses.

## Checked

Method: docs-checked 2026-11-09 against the Software Virtual Textures PDF (sections on translation, feedback, oversubscription, borders, replacement read; other sections skimmed). Dropped the HLSL lookup sketch, D3D12 tiled resource and sampler feedback, Unreal runtime virtual textures, the RTR4 reference, the silverspaceship and Microsoft pages (not read) and claims taken from them.
