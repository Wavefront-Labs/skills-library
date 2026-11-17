---
id: computing-software.game-programming.unreal-engine.blueprint-macros-and-collapsed-graphs
name: blueprint-macros-and-collapsed-graphs
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, blueprint-macro, blueprints, macro-library, collapsed-graph, game-programming]
level: practitioner
status: docs-checked
description: "Create Blueprint macros, Macro Libraries and collapsed graphs, and collapse nodes to a function or macro, following Epic's Macros, Macro Library and Collapsing Graphs pages."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/macros-in-unreal-engine", "https://dev.epicgames.com/documentation/en-us/unreal-engine/blueprint-macro-library-in-unreal-engine", "https://dev.epicgames.com/documentation/en-us/unreal-engine/collapsing-graphs-in-unreal-engine"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Blueprint macros and collapsed graphs

**Goal:** reuse and tidy Blueprint logic with the right container.

## Macros (Macros page)
- A macro is a collapsed network of nodes with entry and exit points set by tunnel nodes; each tunnel can have any number
  of execution or data pins, shown on the macro node.
- Create in a Blueprint Class, Level Blueprint or Macro Library: My Blueprint > + on the macros header, or right-click in
  My Blueprint > Macro. New macros start with an Inputs and an Outputs tunnel node.
- In Details: New under Inputs or Outputs adds execution or data pins (name, type), default values by expanding the entry,
  up/down arrows reorder pins; Description, Category and Instance Color can be set.
- Unlike functions, macros can have more than one output execution pin, and a macro can have no execution pins if it only
  manipulates data and contains no execution nodes.
- Add a macro node: right-click in the graph, drag off a pin with a matching type and direction, or drag from My
  Blueprint. Many copies are allowed; double-click a macro node to open its graph.

## Macro Libraries (Macro Library page)
- A container of macros usable as nodes in other Blueprints, with inputs and outputs for execution and data.
- Create: Content Browser Add > Blueprints > Blueprint Macro Library under Create Advanced Asset (or right-click in the
  Asset View or a folder), then pick a Parent Class. An asterisk on the icon means unsaved.
- Macros are shared among all graphs that reference them but are auto-expanded into graphs like a collapsed node at
  compile time, so a library does not need compiling. Changes to a macro show in referencing graphs only after the
  Blueprint containing them is recompiled.
- Macros stored in a library are accessible to Blueprint Classes and Level Blueprints across the project.

## Collapsing (Collapsing Graphs page)
- Collapse Nodes: select nodes (drag, Ctrl+click to add or subtract), right-click > Collapse Nodes. It becomes a single
  Collapsed Graph node used mainly for organization; hover previews it, double-click opens it, Inputs/Outputs pins can be
  added in Details (Execute is added by default), and right-click > Expand Node reverts.
- Collapse to Function: callable elsewhere with chosen parameters and, with a reference to the owning Blueprint, from a
  different Blueprint. Rename from My Blueprint with F2; Expand Node reverts.
- Collapse to Macro: consolidates connected nodes into one node, "particularly useful for anything that you do frequently,
  like a complex math equation"; Expand Node reverts.

## Checked
Date: 2026-11-07. Read in full: Macros, Blueprint Macro Library and Collapsing Graphs pages (all sections), unversioned
en-us pages with no engine version stated.
Removed as not on those pages: the comparison table (latent nodes in macros, local variables, overridable and RPC-capable
rows), "functions are the default choice" advice, the debugging-clumsiness and macro-library variable-access gotchas,
the pure-function re-evaluation note, wildcard-pin macros, engine macro names (`ForEachLoop`, `DoOnce`, `Gate`), and the
Verify checklist.
Method: documentation only; no commands were run.
