---
id: creative-arts.animation.blender.light-linking-limitations
name: light-linking-limitations
category: creative-arts
field: animation
product: blender
tags: [blender, lighting, light-linking, light-linking-limitations, light-linking-eevee, cycles]
level: practitioner
status: docs-checked
description: "Know Blender light linking limits: emissive meshes Cycles-only, no Grease Pencil, world linking not in 4.0, light tree performance and shadow linking cost."
sources:
  - https://developer.blender.org/docs/release_notes/4.0/cycles/
  - https://docs.blender.org/manual/en/latest/render/lights/light_linking.html
  - https://docs.blender.org/manual/en/latest/render/eevee/object_settings/object_data.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---
# light-linking-limitations

## Limitations

- Light and shadow linking were introduced in **Cycles** in Blender 4.0 (4.0 Cycles release notes). In the 5.2 manual the light/shadow linking collections also appear in the EEVEE Shading panel; the release in which EEVEE gained them is not confirmed here, so check the release notes for your version.
- Linking to the **world** lighting was not supported in 4.0; the 4.0 release notes list it as planned for a future version, so check the notes for your version before relying on it.
- Emissive mesh objects only support light linking with Cycles.
- Grease Pencil objects do not support light linking at all.
- Sampling for light linking is most efficient with the Cycles light tree enabled.
- Shadow linking can make renders slower and trace additional rays, because direct and indirect lighting take different paths.

## Alternatives when unsupported

- View layers with holdouts and separate render passes per light.
- Light groups (`creative-arts.animation.blender.light-groups`) for comp rebalancing.
- Ray visibility per object for global effects.

## Verify

Render the same frame in Cycles and the target engine: compare the linked light contribution; if missing, fall back to view-layer splits.

## Checked

2026-10-27. Documentation release: Blender 5.2 manual (blender-v5.2-release branch) and the 5.2 source UI scripts. Confirmed: Cycles introduction in 4.0 and world linking planned later (4.0 release notes); emissive-mesh and Grease Pencil limits, light tree and shadow-linking performance notes, EEVEE Shading panel entries (Light Linking and EEVEE object settings pages). Removed unsupported claims (export behaviour, set-count limit, Workbench behaviour, indirect-only linking, world linking absence in 5.2).

Method: documentation only; no commands were run.
