---
id: creative-arts.film-live-action.davinci-resolve.node-types-serial-parallel-layer-and-outside
name: node-types-serial-parallel-layer-and-outside
category: creative-arts
field: film-live-action
product: davinci-resolve
tags: [davinci-resolve, resolve, film-live-action, node-types, layer-node-use, outside-node-use, serial-node, parallel-node, splitter-combiner, key-mixer, shared-nodes, compound-nodes]
level: practitioner
status: draft
description: "Use Resolve's node types correctly: serial, parallel and layer mixers, outside nodes, key inputs and key mixer, splitter/combiner, shared and compound nodes, and composite modes."
sources:
  - "https://documents.blackmagicdesign.com/UserManuals/DaVinci_Resolve_Reference_Manual.pdf (Resolve Reference Manual - Node Editor; node types)"
  - "The Colorist Guide to DaVinci Resolve (Blackmagic official training) - node structures"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Node types: serial, parallel, layer and outside

**Goal:** choose the node structure that makes each correction behave predictably -
and keep trees readable for yourself and the next colourist.

## 1. Serial nodes (`Alt/Opt+S`)
Each node processes the output of the previous one. Order matters: balance -> contrast ->
secondary -> look. A secondary keyed on node 3 sees the image as nodes 1-2 left it.

## 2. Parallel nodes (`Alt+P`)
Several nodes receive the **same input** and their outputs are **blended equally** by the
Parallel Mixer. Use for several secondaries on the same base image (sky, skin, car) so
each key is pulled from the same source and they don't affect each other's qualifiers.
Overlapping isolations add together - beware double corrections.

## 3. Layer nodes (`Alt+L`)
Like parallel, but the **Layer Mixer** gives the **bottom input priority** where they
overlap (like layers). Right-click the Layer Mixer for **Composite Mode** (Add, Multiply,
Screen, Overlay, Soft Light...) - e.g. a "Soft Light" layer for a contrast boost, Screen
for glow.

## 4. Outside node (`Alt+O`)
Creates a node after the current one with the **inverse key** of the current node: grade
the subject in node A and everything else in the outside node.

## 5. Keys between nodes
- Each node has a **key input/output** (the small triangle). Drag a node's key output to
  another node's key input to reuse a matte.
- **Key Mixer** combines keys (add, subtract with inversion per input).
- Key palette: **key input gain**, **offset**, **qualifier/ window** combination modes.

## 6. Splitter/Combiner and Alpha
Splitter/Combiner nodes separate R, G, B channels for per-channel operations (e.g.
channel mixing, film-like effects). Alpha output for transparency in Fusion/compositing.

## 7. Organisation
- **Label** every node (right-click > Node Label): "BAL", "CONT", "SKIN", "LOOK".
- **Shared Nodes** (right-click > Save as Shared Node): one node instance across many
  clips - change once, all update (scene looks).
- **Compound nodes**: collapse a group into one node for tidiness.
- Group (pre-clip/post-clip) and Timeline nodes for scene/ show-level work (see groups).
- Save tree templates as PowerGrades.

## Gotchas
- Serial secondaries keyed after a look node, so keys shift when the look changes.
- Parallel nodes double-correcting overlapping areas.
- Unlabelled trees nobody can read in a review.
- Composite modes on the Layer Mixer forgotten - unexpected contrast.

## Verify
- [ ] Node type chosen for its behaviour (serial/parallel/layer/outside).
- [ ] Keys reused via key connections rather than re-pulled.
- [ ] Nodes labelled; shared/compound nodes used for repeated work.
- [ ] Mixer composite modes intentional.
