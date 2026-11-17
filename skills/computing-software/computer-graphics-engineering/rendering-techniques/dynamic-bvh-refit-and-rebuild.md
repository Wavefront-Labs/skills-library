---
id: computing-software.computer-graphics-engineering.rendering-techniques.dynamic-bvh-refit-and-rebuild
name: dynamic-bvh-refit-and-rebuild
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, spatial-structures, bvh-refit, bvh, dynamic-bvh, blas-update, ray-tracing, tree-rotations]
level: advanced
status: docs-checked
description: "Keep BVHs current for moving objects: SAH-guided insertion, tree rotations, enlarged AABBs, remove/re-insert versus refit, Vulkan acceleration structure update flags."
sources: ["https://box2d.org/files/ErinCatto_DynamicBVH_GDC2019.pdf", "https://registry.khronos.org/vulkan/specs/latest/man/html/VkBuildAccelerationStructureFlagBitsKHR.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dynamic BVH refit and rebuild

Source for sections 1 to 3: Erin Catto, "Dynamic Bounding Volume Hierarchies" (GDC 2019, Blizzard
Entertainment), a binary AABB tree used to speed up ray casts and collision queries in a game
world with moving, created, destroyed and streamed objects.

## 1. Cost metric (SAH)
- The probability of a ray hitting a convex object is proportional to its surface area, so the
  surface area heuristic can drive tree construction.
- Tree cost = total surface area of the internal nodes only. Leaf areas and the root area are the
  same for every tree built from the same leaves, so they do not affect comparison.

## 2. Insertion (the key dynamic-tree algorithm)
Three stages: (1) find the best sibling for the new leaf, (2) create a new parent for the sibling
and the leaf (handling the case where the sibling was the root), (3) walk back up refitting
ancestor AABBs.
- Cost of choosing a sibling = surface area of the new parent (direct cost) plus the increase in
  surface area of every ancestor (inherited cost).
- Checking all 2N-1 candidate siblings is too expensive; use branch and bound: recurse with a
  priority queue exploring the best candidates first, keep the best cost so far, and prune a
  subtree when its lower bound (area of the new leaf plus the inherited cost so far) is not below
  the best cost.
- Child order does not matter in a BVH, so swapping left and right gives an equivalent tree.

## 3. Object movement strategies compared
- Refit ancestors: leads to low quality trees.
- Rebuild subtrees: expensive (the talk compares it to garbage collection).
- Remove and re-insert: also expensive, but spread out. The talk chooses this.
- Enlarged ("fat") AABBs: at 60 Hz objects often do not move far per frame, so store an enlarged
  AABB in the tree and only update the leaf when the tight AABB leaves the enlarged one. The
  enlargement scheme is a game-specific choice.
- Sorted insertion order can degrade the incremental SAH tree into a linked list (known since
  Goldsmith and Salmon, 1987). The fix is **tree rotations**: a local operation swapping a node
  with a grandchild (four possible rotations) when that lowers the surface area of the
  intermediate node, applied in stage 3 while walking back up and refitting.

## 4. Vulkan acceleration structure flags
From the Vulkan specification:
- `VK_BUILD_ACCELERATION_STRUCTURE_ALLOW_UPDATE_BIT_KHR`: the structure can later be updated with
  a build `mode` of `VK_BUILD_ACCELERATION_STRUCTURE_MODE_UPDATE_KHR`.
- `PREFER_FAST_TRACE_BIT_KHR` prioritises trace performance over build time;
  `PREFER_FAST_BUILD_BIT_KHR` prioritises build time over trace performance.
- `ALLOW_COMPACTION_BIT_KHR` allows the structure to be a source for a compacting copy.

## Gotchas
- A refit-only tree keeps its original topology, so after large motion (pieces flying apart) quality
  degrades; Catto's remove and re-insert avoids this at the cost of per-object work.

## Verify
- [ ] Compare ray cast time and tree cost (internal node area sum) over an animation with
  different update strategies.
- [ ] Insert objects in sorted order and confirm the tree does not degenerate to a list.

## Checked

Method: docs-checked 2026-11-09 against the Catto GDC 2019 slides (full text read) and the Vulkan VkBuildAccelerationStructureFlagBitsKHR spec page (flag descriptions read). Dropped the DXR flags and Microsoft page (the fetched page had no flag text), the jcgt page (unreadable host), the 1.5-2x SAH rebuild threshold, the TLAS rebuild per frame advice, scratch memory and compaction-with-update claims, and the periodic rebuild interval.
