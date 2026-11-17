---
id: creative-arts.animation.blender.area-splitting-joining
name: area-splitting-joining
category: creative-arts
field: animation
product: blender
tags: [blender, interface, areas, area-splitting, area-join, toggle-maximize-area, window-system, screen-layout]
level: practitioner
status: docs-checked
description: "Split, join, swap, resize, maximise and pop out Blender areas: corner drags, Area Options on the border, Ctrl-Space maximize, Focus Mode and Duplicate Area into New Window."
sources:
  - https://docs.blender.org/manual/en/latest/interface/window_system/areas.html
  - https://docs.blender.org/manual/en/latest/interface/window_system/workspaces.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# area-splitting-joining

Goal: reshape a workspace's screen layout in seconds and recover when a layout gets mangled.

## Basics

The window is divided into areas, each holding an editor; areas are grouped into workspaces. Many shortcuts depend on which editor the cursor hovers over, so move the cursor to the right editor first.

## Docking from a corner

Put the cursor in an area corner (it becomes a cross) and hold `LMB`:
- **Split:** drag left/right to split vertically, up/down to split horizontally. A new area is created.
- **Join:** drag from a corner into a second area; the areas that will be joined are shown brighter.
- Drag a split operation into another area to split and join at once; dragging an area into the middle of a second area replaces the second area with the first.
- `Esc` or `RMB` before releasing cancels.

## Area Options (RMB on a border)

- **Vertical/Horizontal Split:** an indicator line shows where to split; `Tab` switches orientation.
- **Join Up/Down/Left/Right:** shows the join direction overlay.
- **Swap Areas:** swaps this area with the adjacent one.

## Swap, resize

- **Swap contents:** `Ctrl-LMB` on a corner of one area, drag to the target area and release; the areas need not be adjacent but must be in the same window.
- **Resize:** drag a border with `LMB`; hold `Ctrl` to snap to convenient sizes, `Shift` to move nearby aligned borders together.
- Border width and always-visible area handles (useful on touch devices) are options in the interface preferences.

## Maximize, Focus Mode, new window

- **Toggle Maximize Area:** `View > Area > Toggle Maximize Area`, `Ctrl-Spacebar`. The area fills the window; the editor's menu bar and the status bar stay. Return with the shortcut or the *Back to Previous* button in the Topbar. **Restore Area** (`View > Area > Restore Area`) returns to the previous layout.
- **Focus Mode:** `View > Area > Focus Mode`, `Ctrl-Alt-Spacebar`. Fills the window and hides the Topbar, the status bar and the editor's secondary regions (toolbars, sidebars, headers). Return with the shortcut or the icon at the top-right of the editor (visible when hovering).
- **Duplicate Area into New Window:** `View > Area > Duplicate Area into New Window`, or `Shift-LMB` on an area corner and drag outward slightly. The new floating window is a fully functional part of the same Blender instance; useful with several monitors.

## Gotchas

- Layouts are stored per workspace in the .blend. When opening a file, **Load UI** (File Browser option) decides whether the file's screen layout or your current one is used.
- To get a mangled workspace back, use *Duplicate* of a good workspace or add a fresh one from the `+` tab (see `creative-arts.animation.blender.custom-workspaces`).

## Verify

Save and reopen with Load UI enabled: the layout and extra windows return as saved.

## Checked

Date: 2026-10-27. Documentation: Blender manual 5.3 (interface/window_system/areas.rst, interface/window_system/workspaces.rst).
Confirmed: docking, joining, splitting, Area Options names, swap, resize modifiers, Maximize, Restore, Focus Mode (the 5.3 name for the old Toggle Fullscreen Area) and their shortcuts and menu paths, Duplicate Area into New Window, Load UI. Removed unconfirmed claims: `Shift-F1` to `Shift-F12` editor switching, `View > Area > Close Area`, Show Header, a Join Areas border entry, "no reset size command", Text Editor and Python console `Ctrl-Space` conflicts, and Maximize keeping headers and toolbars (the manual says the editor's menu bar and status bar stay).
Method: documentation only; no commands were run.
