---
id: creative-arts.animation.blender.osl-shader-structure
name: osl-shader-structure
category: creative-arts
field: animation
product: blender
tags: [blender, osl-shader-structure, osl-metadata, osl-parameters, osl, script-node, cycles]
level: advanced
status: docs-checked
description: "Write well-formed OSL shaders for Cycles Script nodes: shader signature, input and output parameters, defaults, the supported metadata hints for the UI, and compile errors."
sources:
  - https://docs.blender.org/manual/en/latest/render/cycles/osl/index.html
  - https://docs.blender.org/manual/en/latest/render/shader_nodes/utilities/script.html
  - https://open-shading-language.readthedocs.io/en/main/
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# osl-shader-structure

Goal: an OSL script that compiles first time and shows a clean node UI.

## Anatomy

```c
shader stripes(
    float Scale = 10.0 [[ string label = "Stripe scale" ]],
    color ColorA = color(0.9, 0.9, 0.9),
    color ColorB = color(0.1, 0.1, 0.1),
    int Invert = 0 [[ string widget = "checkBox" ]],
    point Vector = P,                      // defaults to the shading point
    output color Color = 0,
    output float Fac = 0)
{
    float s = sin(Vector[0] * Scale * M_PI);
    Fac = step(0.0, s);
    if (Invert) Fac = 1.0 - Fac;
    Color = mix(ColorB, ColorA, Fac);
}
```

- Each Script node represents one OSL shader; its inputs and outputs are defined by the shader's parameters, and `output` parameters become output sockets.
- Defaults that reference globals such as `P` and `N` are used for the parameter's default.
- Metadata in `[[ ]]` controls the UI. Cycles supports these entries (5.2 manual): `string label = "My Label"` (display name), `string widget = "null"` (hides the parameter), and `string widget = "boolean"` or `"checkBox"` (shows an integer as a checkbox). Other metadata keys are not documented as supported.

## In Blender

1. Render Properties: enable *Open Shading Language* (Cycles).
2. In the Shader Editor add a Script node; Mode *Internal* (a Text data-block) or *External* (`.osl`/`.oso` file or module name).
3. After editing an Internal script press *Script Node Update* to reload it and refresh sockets.

## Compile errors

Compilation errors are shown in the system console.

## Gotchas

- Changing parameter names changes the sockets, which breaks existing links to the old names (the manual suggests wrapping Script nodes in a node group for exactly this reason).
- Use the OSL specification for the available globals (`P`, `N`, `I`, `u`, `v`, `time`) and standard functions.

## Verify

The node shows Scale, ColorA, ColorB, Invert and Vector sockets with the label and checkbox from the metadata; changing Scale updates the render; a deliberate typo prints an error in the console.

## Checked

2026-10-27 against the Blender 5.2 manual (Cycles > Open Shading Language: Usage, Metadata; Script Node page). Corrected: only `label`, `widget = "null"` and `widget = "boolean"/"checkBox"` are documented as supported metadata (removed `min`, `max`, `help`, `widget = "filename"`). Removed unconfirmed claims (automatic stdosl include, node UI limits, status bar errors, node keeping last good sockets, shader name behaviour, world-space globals). Method: documentation only; no commands were run.
