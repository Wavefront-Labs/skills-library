---
id: creative-arts.design-for-form-and-experience.figma.text-colour-and-effect-styles
name: text-colour-and-effect-styles
category: creative-arts
field: design-for-form-and-experience
product: figma
tags: [text-styles, color-styles, effect-styles, figma-styles, grid-styles, shared-styles, typography-styles, figma]
level: practitioner
status: docs-checked
description: "Create and manage Figma text, colour, effect and layout guide styles: creating from objects or local styles, folders, naming for traceability, and when to prefer variables."
sources:
  - "https://help.figma.com/hc/en-us/articles/360038746534"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Text, colour and effect styles

## What styles are
Reusable collections of properties applied to elements. Figma lists these style types: **Colors** (fill, stroke, image, gradient, pattern, shader fill), **Text** (font family, size, line height, spacing), **Effects** (drop shadow, inner shadow, layer blur, background blur, texture, noise, shader effect), **Layout guides** (row, column, grid) and **Animations**, which can only be created from objects in Figma Motion. Styles are available on all plans and creating one needs edit access to the file.

## Create
- **From local styles:** with nothing selected, click the plus next to Local styles in the right sidebar, choose a style type, name it, add a description (shown on hover in the style picker), set the properties and click Create style.
- **From an object:** select it, click Apply styles or variables beside the matching section in the right sidebar, choose New style or variable, name and describe it, and use the minus next to a property to leave it out.
- Organise styles into folders to make them easier to find.
- Name by role and keep names aligned with code tokens for traceability (`creative-arts.design-for-form-and-experience.design-systems.design-tokens-and-a-modular-type-scale`). Colour styles work best with semantic role names rather than raw palette names for component use, with a primitive palette kept separately.

## Practices
- One text style per role; do not rely on ad-hoc mixed sizes.
- Define effects such as shadows as styles (`creative-arts.design-for-form-and-experience.design-systems.defining-elevation-and-radius-scales`).
- Decide between styles and variables per property type (`creative-arts.design-for-form-and-experience.figma.choosing-figma-styles-versus-variables`). Publishing a library is covered in `creative-arts.design-for-form-and-experience.figma.publishing-and-updating-a-figma-library`.

## Verify
- [ ] Every text layer and colour in components uses a style or variable.
- [ ] Names are grouped, semantic and match code.

## Checked
2026-11-01. Confirmed on the Figma Help Center page "Create and edit styles": style types and their properties, plan and edit-access note, both creation paths, descriptions and folders. Removed as unconfirmed: the four-dot icon steps, slash-naming folders, specific style names, the 4-pixel line-height grid, detach, rename, delete and publish behaviour, find-and-replace, and plugin names. Naming and role advice is team convention.
Method: documentation only; no commands were run.
