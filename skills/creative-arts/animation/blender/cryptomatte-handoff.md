---
id: creative-arts.animation.blender.cryptomatte-handoff
name: cryptomatte-handoff
category: creative-arts
field: animation
product: blender
tags: [blender, cryptomatte, cryptomatte-handoff, cryptomatte-metadata, nuke-handoff, exr]
level: practitioner
status: docs-checked
description: "Keep Cryptomatte usable after leaving Blender: the metadata keys Blender writes (name, hash, conversion, manifest), 32-bit float channels, and what to inspect in written EXRs."
sources:
  - https://docs.blender.org/manual/en/latest/render/layers/passes.html
  - https://github.com/Psyop/Cryptomatte
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# cryptomatte-handoff

Goal: compositors can pick Cryptomatte mattes from Blender EXRs in other software.

## What Blender writes

Blender's 5.2 source stores four metadata entries per Cryptomatte layer with the render result: `name` (the layer name), `hash` (`MurmurHash3_32`), `conversion` (`uint32_to_float32`) and `manifest` (the name-to-hash mapping). The Render Layers node outputs half as many Cryptomatte images as the Levels value (for example CryptoObject00, CryptoObject01).

Because the conversion is `uint32_to_float32`, each ID is a 32-bit float bit pattern. Write Cryptomatte layers as **Float (Full)** EXR; a 16-bit half-float file cannot hold a 32-bit pattern (reasoning from the conversion key; the manual does not say this).

## Output path

- The manual's File Output page suggests combining the node with Cryptomatte passes for pipelines, but does not say whether the File Output node preserves the Cryptomatte metadata or layer names. Test a written file before relying on it. Keep the layer names that the manifest expects: do not rename Cryptomatte inputs (see `creative-arts.animation.blender.compositor-file-output`).
- The scene Output Properties can write a multilayer EXR with the passes enabled; compare it with the File Output result when in doubt (practice).
- Avoid tools that strip EXR header attributes when copying or converting files.

## Check

Look at the EXR header in the receiving application or any EXR viewer that lists attributes: you should see the name, hash, conversion and manifest entries for each Cryptomatte layer, and the channels as 32-bit float. In the receiving application, pick an object: its name should appear in the matte list.

## Gotchas

- Renaming a view layer after rendering does not rewrite metadata already written; re-render (practice).
- The Blender Cryptomatte node does not support sidecar metadata files.

## Verify

Open the file in the receiving compositor and pick an object: the name appears and the matte has antialiased edges.

## Checked

Checked 2026-10-27 against the Blender 5.2 manual (blender-v5.2-release branch: render/layers/passes, compositing/types/mask/cryptomatte, compositing/types/output/file_output) and the 5.2 source (blenkernel cryptomatte.cc store_metadata: name, hash, conversion, manifest). Removed unconfirmed claims: the exact `cryptomatte/<key>/` name text in the PDF spec, hash-and-coverage channel pairs, the oiiotool command, and statements about Nuke behaviour. The specification PDF could not be rendered here, so the standard's own wording is not quoted.
Method: documentation only; no commands were run.
