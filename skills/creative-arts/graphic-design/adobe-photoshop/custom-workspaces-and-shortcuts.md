---
id: creative-arts.graphic-design.adobe-photoshop.custom-workspaces-and-shortcuts
name: custom-workspaces-and-shortcuts
category: creative-arts
field: graphic-design
product: adobe-photoshop
tags: [graphic-design, adobe-photoshop, photoshop, photoshop-workspace, photoshop-custom-workspace, photoshop-keyboard-shortcuts, preferences, scratch-disk, performance, history-states, gpu, keyboard-shortcuts]
level: practitioner
status: draft
description: "Set up Photoshop for speed: saved workspaces per task, core and custom shortcuts, and performance settings (RAM, scratch disk, history, GPU)."
sources:
  - https://helpx.adobe.com/photoshop/using/workspace-basics.html
  - https://helpx.adobe.com/photoshop/using/default-keyboard-shortcuts.html
  - https://helpx.adobe.com/photoshop/kb/optimize-photoshop-cc-performance.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Custom workspaces and shortcuts

**Goal:** panels where you need them, hands on the keyboard, and a Photoshop that does not stall.

## Workspaces
- Arrange panels for one kind of task (retouching: Layers, Properties, History, Clone Source;
  compositing: Layers, Channels, Properties, Libraries). Window > Workspace > **New Workspace**,
  tick Keyboard Shortcuts and Menus if you customised them.
- Switch from the workspace menu (top right). **Reset** restores your saved layout after panels drift.
- Tab hides all panels; Shift+Tab hides all but the toolbar; F cycles screen modes.

## Shortcuts worth knowing cold
| Action | Win | Mac |
|---|---|---|
| Brush size / hardness | [ ] / Shift+[ ] | same |
| Brush size and hardness on canvas | Alt+right-drag | Ctrl+Opt+drag |
| Swap colours / default | X / D | X / D |
| Free transform | Ctrl+T | Cmd+T |
| New layer via copy | Ctrl+J | Cmd+J |
| Merge visible to new layer (stamp) | Ctrl+Alt+Shift+E | Cmd+Opt+Shift+E |
| Invert mask/selection | Ctrl+I / Ctrl+Shift+I | Cmd+I / Cmd+Shift+I |
| Fill with foreground / background | Alt+Backspace / Ctrl+Backspace | Opt+Delete / Cmd+Delete |
| Fill dialog (content-aware) | Shift+Backspace | Shift+Delete |
| Step backward (multi-undo) | Ctrl+Z | Cmd+Z |
| Zoom 100% | Ctrl+1 | Cmd+1 |
| Temporary hand / zoom | Space / Ctrl+Space | Space / Cmd+Space |
Number keys set opacity of the active painting tool (or layer with Move tool): 5 = 50%, 0 = 100%.

## Custom shortcuts
Edit > Keyboard Shortcuts (Alt+Shift+Ctrl+K / Opt+Shift+Cmd+K). Save a set; assign F-keys to
frequent menu items (e.g. Select and Mask, Convert to Smart Object). Export the set for other machines.

## Performance preferences (Preferences > Performance)
- Memory: 70-80% of RAM to Photoshop on a dedicated machine.
- **History states:** 50 is a sensible default; more costs RAM and scratch.
- **Scratch disk:** a fast internal SSD other than the system drive if available, with plenty of
  free space (scratch can grow to tens of GB).
- **Use Graphics Processor** on; required for Perspective Warp, Select and Mask speed, smooth zoom.
- Cache levels 4-6 for typical files, higher for very large ones.

## Verify
- [ ] Saved workspaces per task; Reset restores them.
- [ ] Scratch disk on a fast drive with free space; GPU enabled.
