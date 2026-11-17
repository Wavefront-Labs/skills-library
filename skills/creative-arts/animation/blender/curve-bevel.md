---
id: creative-arts.animation.blender.curve-bevel
name: curve-bevel
category: creative-arts
field: animation
product: blender
tags: [blender, curve-object, curve-bevel, bevel-object, bevel-profile, curve-geometry, pipes, cables]
level: practitioner
status: verified
description: "Give Blender curves thickness: Geometry panel Offset, Extrude and Bevel (Round, Object, Profile), Fill Caps, Factor Start/End mapping — pipes, cables, mouldings."
sources:
  - https://docs.blender.org/manual/en/5.2/modeling/curves/properties/geometry.html
  - https://docs.blender.org/manual/en/5.2/modeling/curves/properties/shape.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# curve-bevel

Goal: tubes, cables, frame mouldings and rails from a single curve, editable to the end.

## Properties > Data > Geometry

- **Offset**: moves the control points along their normals.
- **Extrude**: turns the line into a ribbon by extruding to the left and right of the curve normal at each point. Per-point tilt and radius change the direction and distance.
- **Bevel** turns the line (or the Extrude ribbon) into a 3D tube. Three modes:
  - *Round*: circular cross section (a pill when combined with Extrude). **Depth** is the size of the cross section, **Resolution** drives the number of vertices in it (low = blocky), **Fill Caps** seals the ends. Fill Mode *Half* (Shape panel) gives half a cylinder.
  - *Object*: a separate curve object defines the whole cross section; it can be open or cyclic.
  - *Profile*: edit the profile in the curve widget without a second object. The widget defines only a quarter, which is repeated and mirrored. Options: Preset, Reverse Path, Toggle Profile Clipping, Sample Straight Edges, Sample Even Lengths. The *Support Loops* and *Steps* presets depend on Resolution and must be re-applied after changing it.
- **Start & End Mapping**: *Factor Start/End* limit the geometry to a part of the curve (0 to 1); *Mapping Start/End* (Resolution, Segments, Spline) choose how the factor maps to positions. Animate Factor End to grow a vine.
- **Taper Object**, **Taper Radius** and **Map Taper** are covered in the curve-taper skill.

## Bevel Object rules

- The profile curve must be flat in its local XY plane; another plane gives the wrong result.
- Modifiers on the profile curve are ignored: Blender uses the original curve shape. To use a modified profile, turn Bevel off on the path and build the tube with Geometry Nodes (Object Info, Mesh to Curve, then Curve to Mesh with the path and profile).

## Shading and shape

- Active Spline > **Smooth** applies smooth shading to the 3D geometry of the curve.
- A closed (cyclic) curve with Bevel becomes a torus; with a 2D curve and Fill Mode *Both* it becomes a cylinder with rounded edges (this does not work with 3D curves).
- *Resolution Preview U* and *Twist Method* live in the Shape panel (see curve-shape-settings).

## Verify

Toggle wireframe: profile constant along the length; caps closed where Fill Caps is on; change Resolution and re-apply a Profile preset if you use one.

## Checked

Date: 2026-10-27. Documentation: Blender 5.2 manual (Geometry and Shape panels of curve properties). Confirmed: Offset and Extrude behaviour, the three Bevel modes and their settings, Fill Caps, Profile widget quarter/mirror and preset re-apply note, Bevel Object flat-XY requirement and modifier note, Factor Start/End and Mapping options, cyclic/torus and Fill Mode Both examples. Removed as unconfirmed: example depth values, "0 = diamond" resolution, vertex-count formula, UV generation and twist recommendations.
Run check, 2026-11-01, Blender 4.5.14 LTS headless: `bevel_mode` items ROUND, OBJECT, PROFILE; `bevel_depth`, `bevel_resolution` (2 gave an 8-point cross section), `use_fill_caps` (16 faces without, 28 with), `extrude` (a flat curve with Extrude 0.5 gave z from -0.6 to 0.6 with a 0.1 bevel), `offset` (0.3 moved the tube along the normal), `bevel_factor_start/end` (end 0.5 stopped at x = 2 on a 4 m curve), mapping items RESOLUTION, SEGMENTS, SPLINE; a rectangle curve as `bevel_object` produced a 0.4 x 0.2 section; PROFILE mode and `bevel_profile` exist; a cyclic beveled curve closed the tube; 3D fill modes FULL, BACK, FRONT, HALF and 2D fill modes BACK, FRONT, BOTH, NONE; `Spline.use_smooth`. Unrun: Profile widget behaviour and presets, torus and rounded-cylinder shapes, the flat-XY requirement and modifier-ignored note for Bevel Objects, Geometry Nodes alternative (documentation only).

Method: documentation checked against the manual and API pages; the code was run headless in Blender 4.5.14.
