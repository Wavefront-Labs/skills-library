---
id: creative-arts.animation.blender.osl-external-file
name: osl-external-file
category: creative-arts
field: animation
product: blender
tags: [blender, osl-external-file, osl-text, osl, script-node, shader-library, cycles]
level: practitioner
status: docs-checked
description: "Manage OSL code in Blender: Internal text blocks versus External .osl or .oso files, relative paths, the shader search path, node groups for sharing, and enabling OSL for renders."
sources:
  - https://docs.blender.org/manual/en/latest/render/shader_nodes/utilities/script.html
  - https://docs.blender.org/manual/en/latest/render/cycles/osl/index.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# osl-external-file

Goal: keep OSL shaders versioned and reusable without breaking files on other machines.

## Internal

Script node, Mode *Internal*: a Text data-block stores the OSL shader and the compiled OSO bytecode is stored in the node itself. This is useful for distributing a blend-file with everything packed into it. After editing the text, use the node's *Script Node Update* icon: it reloads the text data-block and creates new inputs and outputs if needed.

## External

Mode *External* takes one of three things:
- a path to a `.osl` file, which is automatically compiled into a `.oso` file in the same directory;
- a path to a `.oso` file, used directly, with compilation done manually by you;
- just a module name, looked up in the shader search path (a `shaders/` folder next to the scripts or configuration path of the Blender version in use).

Use relative paths (`//shaders/stripes.osl`) and a shared repository folder so the file resolves on other machines.

## Shader library pattern

Keep one folder of `.osl` files under version control. The manual's production tip: wrap Script nodes in a node group and link that group into other blend-files, so changing sockets later does not require updating every script node in every file. For single-file hand-offs, use Internal mode.

## Gotchas

- A missing External path on a render node breaks the shader; validate that the resolved path exists (`bpy.path.abspath(node.filepath)`) before submitting to a farm.
- The Script node is only evaluated if *Open Shading Language* is enabled in the Render Properties (Cycles), so enable it on every machine that renders the file.
- Compilation errors are shown in the system console.

## Verify

Open the .blend on another machine (or move the project folder): the script node compiles and the console shows no OSL compile errors.

## Checked

2026-10-27 against the Blender 5.2 manual (Script Node and Cycles > Open Shading Language pages). Confirmed Internal/External behaviour, Script Node Update, `.osl`/`.oso`/module-name handling, node-group tip, OSL enable requirement, console errors. Removed unconfirmed claims (include resolution, packing behaviour, version-mismatch behaviour, Make Internal workflow, silent failure colours). Method: documentation only; no commands were run.
