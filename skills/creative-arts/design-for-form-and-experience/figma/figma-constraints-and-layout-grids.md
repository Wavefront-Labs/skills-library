---
id: creative-arts.design-for-form-and-experience.figma.figma-constraints-and-layout-grids
name: figma-constraints-and-layout-grids
category: creative-arts
field: design-for-form-and-experience
product: figma
tags: [figma-constraints, figma-layout-grid, figma-frames, constraints, layout-grids, resizing, responsive-design, figma]
level: practitioner
status: draft
description: "Control how layers resize in Figma frames with constraints, and set up column, row and square layout grids as styles for responsive layouts."
sources:
  - "Figma Help Center - Apply constraints to define how layers resize (help.figma.com/hc/en-us/articles/360039957734)"
  - "Figma Help Center - Layout grids (help.figma.com/hc/en-us/articles/360040450513)"
  - "Figma Help Center - Frames and Resize (help.figma.com)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Constraints and layout grids in Figma

## Constraints
Constraints tell a child layer how to behave when its **parent frame** is resized (not for children of auto layout frames, unless the child uses **absolute position**).
- **Horizontal:** Left, Right, Left & Right (stretches), Center, Scale. **Vertical:** Top, Bottom, Top & Bottom, Center, Scale.
- Pin a close icon to **Top and Right**; make a hero image **Left & Right**; a footer **Bottom** and **Left & Right**; a centred logo **Center**.
- Constraints only matter when you **resize the frame** (drag, or set W/H, or switch frame presets), including for prototyping to different devices; test by dragging the frame edge.
- Constraints reference the **immediate parent frame**; nested frames each have their own; groups ignore them (use frames).
- Use **Clip content** to hide overflow; **Resize to fit** for frames that follow children.

## Layout grids
Select a frame, **Layout grid** (+) in the Design panel (**Ctrl+Shift+4** toggles visibility):
- **Grid:** square grid (size 8) for spacing; **Columns:** count (12 desktop, 8 tablet, 4 mobile), type (**Stretch** with margin, or **Left/Center/Right** fixed width), gutter (24), margin (24-64); **Rows:** for vertical rhythm.
- Layers **snap** to grids; use multiple grids per frame (columns plus an 8-px baseline).
- Save as a **grid style** (four-dot icon) per breakpoint (Desktop-12, Tablet-8, Mobile-4) and share through the library (`creative-arts.design-for-form-and-experience.interaction-design.building-column-grids-and-gutters`).
- Use **guides** (drag from rulers, Shift+R) for one-off alignments.

## Responsive workflow
1. Design at one breakpoint with grid and constraints; **duplicate frames** per breakpoint (360, 768, 1280).
2. Prefer **auto layout with fill/hug** for content (`creative-arts.design-for-form-and-experience.figma.auto-layout-components-and-variants`), constraints for pinned chrome (nav bars, FABs).
3. Test by resizing frames and using **Preview** with device presets.

## Verify
- [ ] Resizing a frame keeps pinned elements pinned and stretchy elements stretchy.
- [ ] Grids saved as styles per breakpoint.
- [ ] No groups where constraints are required.
