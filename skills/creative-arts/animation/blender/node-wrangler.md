---
id: creative-arts.animation.blender.node-wrangler
name: node-wrangler
category: creative-arts
field: animation
product: blender
tags: [blender, node-wrangler, shader-editor, compositor, geometry-nodes, lazy-connect, principled-texture-setup, viewer, node-shortcuts, reroute, lookdev-speed, nw-preview, nw-merge-nodes]
level: practitioner
status: docs-checked
description: "Node Wrangler for Blender node editors: enabling it, Shift W menu, Lazy Connect and Mix, merge shortcuts, Preview Node Output, Principled texture setup, labels, image adders."
sources:
  - https://docs.blender.org/manual/en/latest/addons/node_wrangler.html
licence: Apache-2.0
version: 5
updated: 2026-11-17
aliases: []
---

# node-wrangler

Goal: halve the mouse work in node editors. Node Wrangler (NW) is a bundled add-on: Preferences > Add-ons, search "Node Wrangler", enable. Use its panel in the node editor Sidebar or press **Shift W** for the quick access menu. The shortcut list is in the add-on preferences. Many functions work in the Compositor, Shader, Geometry Nodes and Texture node editors; the manual marks editor-specific ones.

## Shortcuts (default keymap per the manual)

| Keys | Does |
|---|---|
| `Alt RMB` drag | **Lazy Connect**: drag from one node to another; it connects the best-matched sockets by name, type and whether they are free |
| `Shift Alt RMB` drag | Lazy Connect with menus for choosing exact sockets |
| `Shift Ctrl RMB` drag | **Lazy Mix**: connects two nodes' outputs into an appropriate mix-type node |
| `Shift Ctrl LMB` (Shader), `Shift Alt LMB` (Geometry Nodes) | **Preview Node Output**: connects the selected node's output to the Material/World Output (Shader) or final Group Output (Geometry Nodes); click again with the modifiers to cycle outputs |
| `Ctrl T` (Shader) | **Add Texture Setup**: texture node, Texture Coordinate and Mapping onto any shader node; a Background shader gets an Environment Texture |
| `Shift Ctrl T` (Shader) | **Add Principled Setup**: select a Principled BSDF, choose texture files; it adds Image Texture nodes, loads images, sets colour spaces and connects them; map types are detected from file names using tags you can edit in the add-on preferences |
| `Alt S` | **Swap Links** between two selected nodes; with one node selected it cycles or swaps its input links |
| `Alt X` | **Delete Unused Nodes** |
| `Shift P` | **Join Nodes** (into a frame, per `bpy.ops.node.join`) |
| `Alt R` | **Reload Images** used in the tree |
| `Shift C` | Copy settings from the active node to selected nodes of the same type; `Shift V` copies labels |
| `Alt L` / `Shift Alt L` | **Clear Label** / **Modify Labels** (batch add text to start or end, replace text) |
| `/` | **Add Reroutes** to every output of the selected nodes |
| `\` | **Link Active to Selected** (submenu: K to all selected, `'` by node name/label, `;` by output names) |
| `Shift Alt D` | **Detach Outputs** |
| `Shift =` | **Align Nodes** horizontally or vertically |
| `Backspace` | **Reset Nodes** to defaults, keeping connections |
| `Z` (Compositor) | **Reset Backdrop** |
| `[` / `]` | Select the parent frame / the direct children of a frame |

## Merge Selected Nodes

Automatic merge uses Mix for colours, Math for values, and Add/Mix Shader or Join Geometry for specific cases. Modifier signals the node type (`Ctrl` automatic, `Ctrl Alt` Mix node, `Shift Ctrl` Math node); the key signals the operation (Add `=` or Numpad +, Subtract `-`, Multiply `8` or Numpad *, Divide `/`). `Ctrl 0` merges with Mix mode. In the Compositor `Ctrl Numpad .` uses Z-Combine and `Ctrl Alt 0` Alpha Over. Batch Change uses `Alt` plus the operation key to retarget selected Mix or Math nodes, and `Alt Left/Right` changes a Mix factor by 0.1 (`Shift Alt` for 0.01).

## Add images

**Add Multiple Images** (Compositor Add > Input, Shader Add > Texture) adds a node per selected file, useful for importing passes. **Add Image Sequence** needs only one frame of the sequence selected and detects its length.

## Gotchas

- A node-preview connection left wired changes what the output shows; reconnect the real shader to the Output before saving or rendering (practice).
- File names must contain the add-on's map tags for the Principled setup to detect them; adjust the tags in preferences.
- Check Lazy Connect chose the sockets you intended (Color versus Factor).
- Keymap conflicts with other node add-ons or with Emulate 3 Button Mouse (`Alt RMB`) are possible (practice).

## Verify

Preview Node Output on a Noise Texture shows the noise in the viewport. Add Principled Setup on a Principled BSDF with a set of PBR texture files wires the maps with sensible colour spaces. Delete Unused Nodes removes only dangling nodes.

## Checked

Checked 2026-10-27 against the Blender 5.2 manual (blender-v5.2-release) addons/node_wrangler.rst (enable steps, Shift W, every shortcut in the table, merge modifiers, preview shortcuts per editor, tag editing, image adders). Removed unconfirmable items from the earlier draft: Shift S Switch Node Type, O Link to Output (the manual mentions Connect to Output without a key), Shift P as Frame Selected (the manual says Join Nodes), Ctrl Numpad . as Mix merge (it is Z-Combine), the Clear Viewer operator, preference names (Merge Position etc.), specific map tags, native shortcut list and Specular IOR Level note. Method: documentation only; no commands were run.
