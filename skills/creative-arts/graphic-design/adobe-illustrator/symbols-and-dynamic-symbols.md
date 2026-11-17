---
id: creative-arts.graphic-design.adobe-illustrator.symbols-and-dynamic-symbols
name: symbols-and-dynamic-symbols
category: creative-arts
field: graphic-design
product: adobe-illustrator
tags: [graphic-design, adobe-illustrator, illustrator, ai-symbols, dynamic-symbols, symbol-instances, symbol-sprayer, 9-slice-scaling]
level: practitioner
status: draft
description: "Reuse artwork with Illustrator symbols: static vs dynamic symbols, editing masters, overriding instance appearance, symbol tools, 9-slice scaling and breaking links."
sources:
  - https://helpx.adobe.com/illustrator/using/symbols.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Symbols and dynamic symbols

**Goal:** many instances of one master; edit once, update everywhere.

## Creating
Select art, Symbols panel (Shift+Ctrl/Cmd+F11) > New Symbol, or drag in.
- Export Type: Movie Clip/Graphic (only matters for Flash/Animate export).
- **Symbol Type: Dynamic Symbol** (default) or Static.
- Enable Guides for **9-Slice Scaling** - corners stay unscaled (buttons, frames).
- Registration point for rotation/scale origin.

## Static vs Dynamic
- **Static**: instances identical; editing the master updates all.
- **Dynamic**: each instance can override appearance (fill, stroke colours, opacity) with the
  Direct Selection tool while keeping the shape linked to the master. Edit master shape -> all update;
  overridden colours persist. Reset in Properties.

## Editing
- Double-click an instance to edit the master in Isolation mode.
- Replace: select instances, Properties > Replace with another symbol.
- **Break Link** turns an instance into plain artwork.

## Symbolism tools
Symbol Sprayer, Shifter, Scruncher, Sizer, Spinner, Stainer, Screener, Styler - scatter
foliage, crowds, confetti. Expand to edit individual pieces.

## Gotchas
- SVG export writes symbols as `<symbol>`/`<use>` - efficient, but some importers flatten them.
- Libraries panel graphics are a different mechanism (CC Libraries), not symbols.

## Verify
- [ ] Editing the master changes every instance; overrides remain on dynamic instances.
