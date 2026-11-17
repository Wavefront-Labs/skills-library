---
id: creative-arts.graphic-design.information-design.flowcharts-and-decision-trees
name: flowcharts-and-decision-trees
category: creative-arts
field: graphic-design
product: information-design
tags: [graphic-design, information-design, diagram-design, flowchart, decision-tree, process-diagram, iso-5807, swimlane, connectors, diagram-layout, illustrator, figma]
level: practitioner
status: draft
description: "Design readable flowcharts and decision trees: standard shapes (ISO 5807), one reading direction, orthogonal connectors, swimlanes, consistent spacing and labelled decisions."
sources:
  - https://www.iso.org/standard/11955.html
  - https://www.edwardtufte.com/book/envisioning-information/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Flowcharts and decision trees

**Goal:** a reader follows any path from start to end without hunting for the next step.

## Structure first (on paper or in text)
1. List the steps and decisions in order. Each decision has **mutually exclusive, labelled
   outcomes** (Yes/No, or named options).
2. Identify the main ("happy") path - it should run straight; exceptions branch off it.
3. Count the nodes: over ~25, split into linked sub-charts.

## Shapes (ISO 5807 / common convention)
- **Terminator** (rounded rectangle/pill): start, end.
- **Process** (rectangle): an action, verb first ("Check ID").
- **Decision** (diamond): a question; outcomes on its exits. For text-heavy designs, a
  rectangle with a question mark and a distinct colour is more legible than a cramped diamond.
- Data/input (parallelogram), document, subprocess (double-sided rectangle), connector (circle
  with a letter for off-page jumps).
Use as few shape types as the audience needs; public-facing charts often use just three.

## Layout rules
- **One direction:** top-to-bottom or left-to-right. Main path straight down the middle.
- **Orthogonal connectors** (right angles), arrowheads at the end only, no crossing lines -
  reroute or reorder to remove crossings; if one is unavoidable, use a line hop.
- Equal spacing between nodes; align centres on a grid. Same box width per column where possible.
- Label every exit of a decision near the diamond, not mid-line.
- **Swimlanes** (rows/columns per role or system) when "who does it" matters.

## Decision trees
For "which option fits me?" content: questions as nodes, answers as branch labels, outcomes as
leaf boxes with distinct colour. Keep each level's questions parallel in wording.

## Tools
- Illustrator: Smart Guides, Align/Distribute (spacing values), connectors drawn with the
  Line tool and pen; use symbols for repeated nodes.
- Figma/FigJam: auto-connectors stick to nodes and reroute when moved; components for node types.
- For engineering audiences, diagram-as-code (Mermaid, Graphviz) keeps charts in sync with text.

## Verify
- [ ] Every path from start reaches an end; no orphan nodes.
- [ ] No line crossings; every decision exit labelled.
- [ ] A first-time reader can trace three random scenarios correctly.
