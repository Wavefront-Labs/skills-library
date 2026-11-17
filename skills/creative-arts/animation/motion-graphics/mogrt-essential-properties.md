---
id: creative-arts.animation.motion-graphics.mogrt-essential-properties
name: mogrt-essential-properties
category: creative-arts
field: animation
product: motion-graphics
tags: [essential-properties, mogrt, motion-templates, essential-graphics-panel, after-effects, premiere-pro, template-controls, lower-third-template]
level: practitioner
status: draft
description: "Build Motion Graphics templates (.mogrt) in After Effects with Essential Graphics: exposing text, colour and checkbox controls for editors in Premiere Pro."
sources:
  - https://helpx.adobe.com/after-effects/using/creating-motion-graphics-templates.html
  - https://helpx.adobe.com/premiere-pro/using/working-with-motion-graphics-templates.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Mogrt and Essential Properties

**Goal:** editors change names, titles and colours of show graphics in Premiere Pro without opening
After Effects, while the animation stays locked to the design.

## Building the template

1. Build the graphic in one master comp (lower third, title card, end card).
2. Window - **Essential Graphics**. Set the Primary comp (Solo Supported Properties helps find
   what can be exposed).
3. Drag properties into the panel: Source Text (text field), Fill colour (colour picker), Slider
   Control values, Checkbox Control (toggle elements), Dropdown Menu Control (style variants),
   Position/Scale (point/slider), media replacement (comp layers marked for replaceable media).
4. Rename each control clearly ("Name", "Title", "Accent colour"); group related controls.
5. Set the poster frame, then **Export Motion Graphics Template** to a local library or a
   Creative Cloud library for the team.

## Essential Properties inside AE

When the master comp is nested in another AE comp, exposed controls appear as **Essential Properties**
on the nested layer (twirl down). Each instance can have different text/colour without duplicating
the precomp: the AE-side equivalent of a mogrt.

## Design rules for templates

- Use expressions so layout adapts to text length (`sourceRectAtTime`), see
  `creative-arts.animation.motion-graphics.responsive-design-mogrt`.
- Lock what editors must not change (fonts, timing) by simply not exposing it.
- Include all fonts or use Adobe Fonts; missing fonts on an editor's machine break the look.
- Keep templates light: avoid heavy precomps and third-party plug-ins (editors may not have them).

## Gotchas

- Changing the template after editors used it: Premiere keeps the old version in projects already
  using it; version names (`LowerThird_v02`) and tell editors to replace.
- Dropdown menu controls drive expressions; editors see labels, the expression reads index 1..n.
- Text fields with line breaks need the text box design to allow them.

## Verify

Install the .mogrt on another machine with Premiere, change every exposed control, render a few
variants: layout adapts, no missing font or effect warnings.
