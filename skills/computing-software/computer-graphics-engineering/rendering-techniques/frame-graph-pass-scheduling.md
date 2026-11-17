---
id: computing-software.computer-graphics-engineering.rendering-techniques.frame-graph-pass-scheduling
name: frame-graph-pass-scheduling
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, efficient-shading, pass-scheduling, frame-graph, render-graph, transient-resources, resource-barriers, async-compute]
level: advanced
status: docs-checked
description: "Bake a render graph for Vulkan as in Granite: dependency traversal, pass reordering, subpass merging, barrier building, image aliasing and async compute queues."
sources: ["https://themaister.net/blog/2017/08/15/render-graphs-and-vulkan-a-deep-dive/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Frame graphs and pass scheduling

Source: Hans-Kristian Arntzen (themaister), "Render graphs and Vulkan: a deep dive" (2017), the
render graph of the Granite engine. The frame is a graph of passes with declared resource inputs
and outputs; a bake step turns it into an executable order with barriers and shared memory. The
article's baking steps, in order:

1. **Validate** pass structures. If colour input and output dimensions differ, the pass can use a
   scaled blit at the start instead of loadOp LOAD (loadOp becomes DONT_CARE), for example game
   at low resolution then UI at native resolution.
2. **Traverse the dependency graph** (assumed acyclic) bottom-up starting from the passes that
   write the backbuffer, pushing the passes that write each of their resources, recursively;
   reverse the list and prune duplicates. This gives a valid submission order, not yet an
   optimal one. Passes that are good merge candidates (for example lighting using input
   attachments from the G-buffer pass) are noted.
3. **Reorder passes.** Optimisation metric: maximise the number of passes between a writer and
   its reader, to minimise hard barriers. Each unscheduled pass is scored: a merge candidate
   scores infinite; otherwise the score is how many passes can overlap in between with the
   latest scheduled pass it must wait for; passes that would break the dependency chain are
   skipped. To keep subpass merging working, dependencies of merge candidates are lifted to the
   first pass in the merge chain.
4. **Logical-to-physical resources.** Read-modify-write resources are aliased to the same
   physical resource (a logical split exists only to name resources and avoid cycles).
5. **Merge render passes** when both are graphics passes, they share colour, depth or input
   attachments, there is at most one unique depth/stencil attachment, and their dependencies
   can be expressed by region (BY_REGION_BIT, no arbitrary-location texture sampling). This
   matters most on tile-based renderers.
6. **Transient attachments:** a resource used in only one physical render pass that never needs
   storeOp STORE and is invalidated at the start (no loadOp LOAD) can avoid physical memory on
   tilers.
7. **Build barriers.** Per pass, inputs go into an invalidate bucket (for example fragment stage,
   shader read access, shader-read-only layout) and outputs into a flush bucket (for example
   colour-attachment-output stage, colour write access, colour-attachment-optimal layout);
   read-modify-write resources go in both. A resource that is only read gets a fake flush
   barrier with access 0 so later writers still wait for the readers (back-to-back readers in
   the same layout need no barrier). A write-only resource can be discarded by transitioning
   from UNDEFINED, and still needs an invalidate barrier for the layout transition. Barriers
   between merged subpasses are handled by subpass dependencies.
8. **Render target aliasing:** find the first and last physical pass using each resource; two
   resources with the same dimensions and format whose pass ranges do not overlap can alias
   (the separable blur ping-pong example). Ownership is handed over by copying the barriers to the next
   alias and forcing layout UNDEFINED, in a ring over frames. Caveats: history or feedback images
   (current plus previous frame) must never alias; aliasing can add barriers and reduce
   throughput; maximising pass overlap reduces aliasing opportunities.
9. **Async compute:** resources used by both graphics and compute queues in different queue
   families need EXCLUSIVE or CONCURRENT sharing; the author chose CONCURRENT only for resources
   truly used in both, because exclusive ownership transfer is complicated.

At runtime the graph checks conditional execution, handles discard and invalidate barriers,
executes the render passes, handles flush barriers and alias handoff, then submits.

## Gotchas
- Imported or history resources need explicit lifetimes and must not alias.
- Optimising purely for pass overlap and for memory aliasing conflict; decide which wins knowing
  your VRAM budget at bake time.

## Verify
- [ ] Validation layers clean on barriers and layouts.
- [ ] A history (TAA) image is never aliased.

## Checked

Method: docs-checked 2026-11-09 against the themaister Granite render graph article (baking section read in full; the problem statement and runtime sections skimmed). Dropped the Frostbite GDC and Unity pages (not read), the C++ builder sketch, pass culling by reference counts, D3D12 placed resource aliasing, UE RDG and Filament claims, and the Graphviz and compile caching advice.
