---
id: computing-software.web-development.web-accessibility.dragging-movements-alternatives
name: dragging-movements-alternatives
category: computing-software
field: web-development
product: web-accessibility
tags: [input-modalities, pointer-accessibility, dragging-movements, wcag-2-5-7, drag-and-drop-alternative, sortable-list, keyboard-reorder, wcag-2-2, keyboard-drag-drop]
level: practitioner
status: docs-checked
description: "Meeting WCAG 2.2 SC 2.5.7 Dragging Movements: single-pointer alternatives to drag-and-drop for sortable lists, kanban boards, sliders and resizers."
sources:
  - https://www.w3.org/WAI/WCAG22/Understanding/dragging-movements.html
  - https://www.w3.org/WAI/ARIA/apg/patterns/slider/
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Dragging movements alternatives (WCAG 2.5.7)

**Goal:** anything done by dragging can be done with single taps/clicks (new AA criterion in WCAG 2.2).

## 1. Scope
Dragging = press, move, release at another point. 2.5.7 requires a **single-pointer** alternative without dragging (tap/click based), unless dragging is essential (freehand drawing). Keyboard support alone does **not** satisfy it (it's for pointer users who can't drag precisely).

## 2. Patterns
| Drag UI | Alternative |
|---|---|
| Sortable list | "Move up"/"Move down" buttons, or a "Move to position…" select |
| Kanban card between columns | Card menu: "Move to > In progress" |
| Slider thumb | Click on the track to jump; +/- buttons; typed input |
| Resizable panel | Buttons or a preset menu (Small/Medium/Large); double-click to reset |
| Drag to upload | File picker button (already standard) |
| Map pan | Arrow buttons |
| Range selection on a chart | Inputs for start/end |

## 3. Implementation
- Keyboard support (2.1.1) is separate: add the tap-based single-pointer alternative yourself even if your drag library has keyboard sensors.
- Announce result of moves via live region: "Moved 'Write tests' to position 3 of 7" / "to In progress".
- Keep focus on the moved item after the move.

```jsx
<li>
  {task.title}
  <button aria-label={`Move ${task.title} up`} onClick={() => move(i, i-1)} disabled={i===0}>↑</button>
  <button aria-label={`Move ${task.title} down`} onClick={() => move(i, i+1)} disabled={i===last}>↓</button>
</li>
```
(Name starts with "Move" - icon buttons; tooltip text should match.)

## 4. Target size
Alternative controls also need 24x24 CSS px (2.5.8) or spacing.

## Verify
- [ ] Every drag interaction can be completed with clicks only (try with a trackpad, no dragging).
- [ ] Moves are announced and focus stays on the item.
- [ ] Keyboard-only also works (2.1.1).

## Checked

2026-10-26, against WCAG 2.2 normative text and Understanding documents (w3c/wcag repository, checked 2026-10-26). Confirmed from the normative text and Understanding page of 2.5.7 Dragging Movements (Level AA, new in WCAG 2.2): a single pointer without dragging, unless essential; the Understanding page states the requirement is separate from keyboard accessibility and gives the slider-track click as an example. Removed the library-capability claims and the dnd-kit source.

Method: documentation only; no commands were run.
