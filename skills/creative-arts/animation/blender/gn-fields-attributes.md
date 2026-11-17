---
id: creative-arts.animation.blender.gn-fields-attributes
name: gn-fields-attributes
category: creative-arts
field: animation
product: blender
tags: [blender, geometry-nodes, gn-fields, fields-concept, field-evaluation, gn-named-attributes, store-named-attribute, capture-attribute, attributes]
level: practitioner
status: verified
description: "Reason about Geometry Nodes fields (diamond vs circle sockets, evaluation context, domains) and pass data through a tree with Store Named Attribute and Capture Attribute."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/fields.html
  - https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/attribute/store_named_attribute.html
  - https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/attribute/capture_attribute.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# gn-fields-attributes

Goal: understand *when* a field is evaluated and *on what*, so values come out right after topology changes. General GN setup is in `geometry-nodes`.

## Fields in one page

- **Diamond socket** = field (a function evaluated per element later); nodes with diamond inputs and outputs are field nodes. A link coming from a field socket is drawn dashed, otherwise solid.
- A field is evaluated by the node it plugs into, on *that node's* geometry and domain: Set Position evaluates Position/Normal/Index on the point domain of the geometry entering Set Position.
- The same field (e.g. Index) gives different results in different nodes — follow the dashed lines back to see which geometry it belongs to.
- **Domains**: Point, Edge, Face, Face Corner, Spline, Instance, Layer. Attributes are interpolated automatically between domains, normally by simple averages (Booleans have special rules, e.g. a face is selected from points only if all its vertices were).
- A solid red link marks an invalid field connection. To get one value from a field use Sample Index or Attribute Statistic.

## Capture Attribute (anonymous, in-tree)

Stores one or more fields as an anonymous attribute on the geometry, so a value survives a change that would otherwise lose or re-evaluate it, e.g. capture the initial Position before Set Position nodes. Pick the **Domain**; items are managed in the *Capture Items* list. The 4.5.14 Capture Attribute node has no Selection input (the 5.x manual lists one). The captured attribute is only available on the geometry produced by this node, not in sibling or upstream nodes.

## Store Named Attribute (persistent, named)

- Writes a named attribute of a chosen **Data Type** and **Domain**; read it later with **Named Attribute** or in the Spreadsheet. An existing attribute has its data type and domain updated, except built-in attributes, whose domain and type cannot change.
- *Selection*: if the attribute does not exist, unselected elements are zero-filled; otherwise only selected elements change.
- Capture Attribute is preferable for reuse inside one tree because it cannot clash with names on the input geometry.
- Use Remove Named Attribute to clean up before export.

## Gotchas

- Store on the domain you will read: reading a Point attribute on the Face domain averages it.
- Instance-domain attributes only exist in geometry nodes; realise instances before relying on attributes elsewhere.
- Field sockets connected to the Group Output create output attributes in the modifier (domain set in the output properties); this does not work with instanced data. Store Named Attribute is the alternative.

## Verify

Spreadsheet (right domain) shows the attribute column; a Viewer node (`Shift-Ctrl-LMB` on a socket) displays the field on the geometry.

## Checked

2026-10-27, against the Blender 5.3 manual (branch blender-v5.3-release). Confirmed on the Fields, Attributes Reference, Capture Attribute, Store Named Attribute, Viewer and Geometry Nodes modifier pages: dashed or solid links, red error links, domain list and interpolation, Capture and Store Named behaviour, Group Output attributes still supported. Removed the claim that Group Output attributes were replaced, the diamond-with-dot description, version gates and the shader Instancer claim.

Run check, 2026-11-01, Blender 4.5.14 LTS headless (bpy, factory settings): attribute domains Point, Edge, Face, Face Corner, Spline, Instance, Layer on Capture Attribute and Store Named Attribute; Capture Attribute has a capture_items list. Evaluated Store Named Attribute on a 4-point line: storing 5 with selection Index<2 into a new attribute gave [5, 5, 0, 0] (unselected zero-filled), then storing 9 with selection Index=3 into the existing attribute gave [5, 5, 0, 9]. Wrong in the old text: Capture Attribute has no Selection input in 4.5.14. Not run (confirmed from the manual only): dashed and red link drawing, domain interpolation rules, Group Output attributes, Viewer node use.

Method: manual text confirmed from documentation; the listed behaviour run headless in Blender 4.5.14.
