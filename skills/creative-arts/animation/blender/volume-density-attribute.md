---
id: creative-arts.animation.blender.volume-density-attribute
name: volume-density-attribute
category: creative-arts
field: animation
product: blender
tags: [blender, volume-density-attribute, density-attribute, flame-attribute, temperature-attribute, volumetrics, openvdb]
level: advanced
status: docs-checked
description: "Drive volume shading from grids and attributes: default grid names, Principled Volume attribute inputs, blackbody emission, and the Attribute node."
sources:
  - https://docs.blender.org/manual/en/latest/render/shader_nodes/shader/volume_principled.html
  - https://docs.blender.org/manual/en/latest/modeling/volumes/introduction.html
  - https://docs.blender.org/manual/en/latest/render/shader_nodes/input/attribute.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---
# volume-density-attribute

Goal: shade imported or simulated volumes correctly instead of a uniform grey box.

## Grids
A grid is a set of volumetric data; it typically stores the density of each voxel but can also hold temperatures, velocities and so on. For a Volume object, the Object Data > Grids list shows each grid's name and data type. Volume objects render with Principled Volume by default, using grids named `density`, `color` and `temperature`; if these are not available, choose another grid name in the shader nodes. Volumes come from OpenVDB files (for example from Houdini) or from Blender's fluid simulation cache.

## Principled Volume inputs
- **Density** and **Density Attribute** (grid defining the density, typically "density").
- **Color** (scattering colour) and **Color Attribute** (grid for colouring; use "color" for smoke simulations).
- **Anisotropy** (backward or forward scattering direction), **Absorption Color** (shadow colour tint).
- **Emission Strength** and **Emission Color**.
- **Blackbody Intensity** (set to 1 for physically accurate intensity), **Blackbody Tint**, **Temperature** (kelvin; higher emits more) and **Temperature Attribute** (grid, typically "temperature").
The Volume output goes to the Volume input of the Material Output (or World Output).

## Attribute node
Input > Attribute, **Attribute Type** *Geometry* for data that varies within the volume of the object, **Name** = the grid or attribute name. Outputs: Color, Vector, Factor, Alpha (Alpha defaults to 1 if the attribute has no alpha). Use the Factor output to remap a grid (for example through a Color Ramp or Map Range) into Density or Emission inputs.

## Gotchas
- Names must match the grid names listed in the Grids list.
- Importing OpenVDB points is not supported, and level set grids can be read but not rendered as surfaces.

## Verify
Plug an Attribute node's Factor into Emission Strength to visualise a grid; the render should show the expected distribution with no box-shaped boundary.

## Checked
Date: 2026-10-27. Documentation: Blender manual (Principled Volume, Volume introduction, Attribute node), branch blender-v5.2-release. Confirmed: default grid names, all Principled Volume inputs and their descriptions, Attribute node type, name and outputs, limitations. Removed unconfirmed claims: Mantaflow grid names flame and heat, Houdini and EmberGen naming, normalised-temperature remark, the 1000 to 6000 K remap range, the fire node recipe and EEVEE attribute remark.
Method: documentation only; no commands were run.
