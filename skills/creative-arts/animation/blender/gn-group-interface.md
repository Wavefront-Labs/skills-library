---
id: creative-arts.animation.blender.gn-group-interface
name: gn-group-interface
category: creative-arts
field: animation
product: blender
tags: [blender, geometry-nodes, gn-group-interface, group-inputs, node-panels, gn-index-menu-switch, index-switch, menu-switch, node-groups]
level: practitioner
status: verified
description: "Design a clean Geometry Nodes group interface: socket defaults, subtypes, panels, hide-value, single-value vs field inputs, plus Menu Switch dropdowns and Index Switch."
sources:
  - https://docs.blender.org/manual/en/latest/interface/controls/nodes/groups.html
  - https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/utilities/menu_switch.html
  - https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/utilities/index_switch.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# gn-group-interface

Goal: a node group that an artist can use from the modifier panel (or as an asset) without opening the tree.

## Interface (sidebar, Group tab, Group Sockets panel)

The interface item list holds inputs, outputs and panels. Per socket:

- **Type**, **Description** (the tooltip shown on hover), **Default**, **Min**, **Max** (limits of the UI control).
- **Subtype** for integer, float, vector and string sockets (for floats: None, Pixel, Percentage, Factor, Mass, Angle, Time, Distance and more). It changes display and units, not the data type.
- **Hide Value** hides the socket's value control even when unconnected. **Default Input** (Integer, Vector, Matrix, Object inputs; requires Hide Value) chooses what an unconnected input receives, for example Index, ID or Index, Normal or Self Object.
- **Hide in Modifier** keeps an input inside the group but out of the modifier panel.
- **Structure Type**: *Auto*, *Single* (constants only), *Dynamic*, *Field* or *Grid* (the 4.5.14 enum has all five) decide what can be connected.
- **Default Attribute** and **Attribute Domain** (outputs) set the attribute name and domain used when the group is a modifier.
- **Panels** group sockets and sit at the bottom of the node; nest by dragging one panel onto another. *Closed by Default* collapses a panel on new nodes. A **Panel Toggle** adds a boolean checkbox to the panel header.

Order matters: Geometry first, then the most tweaked parameters.

## Menu Switch

Menu Switch outputs one input chosen by a menu. Menu items are defined in the sidebar and can be added, removed, renamed (existing links are kept) and reordered. Connecting its Menu input to a Group Input exposes a dropdown in the group and in the modifier. It hides sockets that are connected only to inactive inputs, so settings for unused variants disappear from the modifier. Two different Menu Switch nodes feeding the same menu socket conflict; wrap the switch in one node group and reuse that group.

## Index Switch

Outputs one of its inputs by a zero-based integer *Index*. If the index is outside the available inputs the output is the first input or a zero-equivalent, depending on type. Connect Index to a Menu Switch of type Integer and the menu labels show next to the index value.

## Asset-ready groups

- *Usage* (sidebar Group tab, Geometry Nodes): **Modifier** for use in the Geometry Nodes modifier, **Tool** for node tools. Disabling both hides the group from the editor lists.
- The 5.x manual describes a *Show Manage Panel* option; the 4.5.14 node tree has no such property, so it was not run.
- Add a group *Description* and a catalogue for discoverability.

## Gotchas

- Changing a socket type breaks existing links and modifier values on every user.
- Field inputs show a toggle in the modifier switching between a single value and an attribute name.
- The modifier's Inputs panel lists the group inputs per modifier even when the group is shared.

## Verify

Use only the modifier panel: all needed controls exist, units display properly, the dropdown switches variants.

## Checked

2026-10-27, against the Blender 5.3 manual (branch blender-v5.3-release). Confirmed against the Node Groups page (Group Sockets, Usage, Show Manage Panel), Menu Switch, Index Switch and Geometry Nodes modifier pages. Removed unconfirmed version gates and the claim that Modifier usage adds the group to the Add Modifier menu.

Run check, 2026-11-01, Blender 4.5.14 LTS headless (bpy, factory settings): interface socket properties description, default_value, min_value, max_value, subtype, hide_value, hide_in_modifier, default_input, structure_type (AUTO, SINGLE, DYNAMIC, FIELD, GRID), default_attribute_name, attribute_domain, is_panel_toggle; panels have default_closed; node tree properties is_modifier and is_tool (Usage); Menu Switch has an item list with Menu input; Index Switch with a Float type returned zero for an out-of-range index. Wrong or missing in the old text: Dynamic structure type omitted, and Show Manage Panel is not a 4.5.14 property. Not run (confirmed from the manual only): sidebar layout, Hide Value requirement for Default Input, link conflict between two Menu Switch nodes, asset catalogue use.

Method: manual text confirmed from documentation; the listed behaviour run headless in Blender 4.5.14.
