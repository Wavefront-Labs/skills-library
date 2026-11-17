---
id: computing-software.game-programming.godot.ui-containers-and-size-flags
name: ui-containers-and-size-flags
category: computing-software
field: game-programming
product: godot
tags: [godot, godot4, godot-ui, godot-containers, size-flags, anchors, control-node, margincontainer, vboxcontainer, layout, game-programming]
level: practitioner
status: docs-checked
description: "Lay out Godot UI with Containers instead of manual positions: anchors presets, Box/Grid/Margin containers, size flags expand/fill/ratio, minimum sizes and scroll lists."
sources: ["https://docs.godotengine.org/en/stable/tutorials/ui/gui_containers.html", "https://docs.godotengine.org/en/stable/tutorials/ui/size_and_anchors.html", "https://docs.godotengine.org/en/stable/classes/class_control.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# UI containers and size flags

**Goal:** menus and HUDs that adapt to any window size and content length without hand-placed
coordinates.

## Two layout systems
1. **Anchors and offsets** for a Control whose parent is *not* a Container: anchor presets
   (Layout toolbar: Full Rect, Top Left, Center...) pin it relative to the parent rect.
2. **Containers** control their children's position and size: children give up their own positioning
   and manual changes are ignored or invalidated at the next resize. Use containers for anything
   list-like or resizable.

## Container toolbox
| Container | Does |
|---|---|
| `MarginContainer` | Padding (theme constants `margin_left`...). Typical screen root under a Full Rect anchor. |
| `VBoxContainer` / `HBoxContainer` | Stack children; `separation` constant. |
| `GridContainer` | `columns` count grid (inventory). |
| `CenterContainer` | Centers child at its minimum size. |
| `PanelContainer` | Draws a StyleBox, then expands its children to cover the area (respecting the StyleBox margins). |
| `ScrollContainer` | Scrolls one child (usually a VBox) larger than itself. |
| `AspectRatioContainer` | Keeps ratio (portraits, minimaps). |
| `HFlowContainer` / `VFlowContainer` | Wrapping rows (tags, buttons). |
| `HSplitContainer` / `VSplitContainer`, `TabContainer` | Draggable grabbers between children; stacked children with tabs (only the current one visible). |

## Size flags (per child, horizontal and vertical)
- **Fill**: take the whole space allocated to it.
- **Expand**: claim leftover space in the container (shared among expanding siblings).
- **Stretch Ratio**: share of leftover space among expanding siblings (2 = twice as much).
- **Shrink Begin/Center/End**: keep minimum size and align.
Typical: a label + value row in an HBox: label `Expand+Fill`, value `Shrink End`.

## Minimum sizes
Set `custom_minimum_size` on elements that need a guaranteed size; containers lay children out from
their minimum sizes.

## Example: pause menu
```
CanvasLayer
  Control (Full Rect)                 # dim background ColorRect also Full Rect
    CenterContainer (Full Rect)
      PanelContainer
        MarginContainer
          VBoxContainer (separation 12)
            Label "Paused"            # horizontal_alignment center
            Button "Resume"           # size flags H: Fill
            Button "Settings"
            Button "Quit"
```

## Building lists in code
```gdscript
for item in items:
    var row := preload("res://ui/item_row.tscn").instantiate()
    row.setup(item)
    $Scroll/List.add_child(row)       # container positions it; never set row.position
```

## Verify
- [ ] Resize the window from 800x600 to 3440x1440: nothing overlaps or leaves the screen.
- [ ] Long translated strings wrap or expand without clipping.
- [ ] No Control under a Container has a manually set position.

## Checked

Checked 2026-10-25 against the Godot 4.7 documentation (godot-docs stable branch, last commit 2026-10-24; latest engine release 4.7.2). Confirmed: children of a Container give up their own positioning; size flags Fill, Expand, Shrink Begin/Center/End and Stretch Ratio semantics (2 takes twice the space of 1); Box containers use Stretch Ratio; GridContainer needs a column count; MarginContainer margins and Box separation are theme constants; TabContainer, HSplitContainer/VSplitContainer, PanelContainer, ScrollContainer (single child, per-axis scrolling), AspectRatioContainer, HFlowContainer/VFlowContainer and CenterContainer (centres children at minimum size) behaviours; anchor presets. Removed the unconfirmed editor-greying, 48 px and autowrap claims.

Method: documentation only; no commands were run.
