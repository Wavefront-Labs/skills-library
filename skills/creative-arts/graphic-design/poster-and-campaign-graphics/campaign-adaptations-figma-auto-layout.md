---
id: creative-arts.graphic-design.poster-and-campaign-graphics.campaign-adaptations-figma-auto-layout
name: campaign-adaptations-figma-auto-layout
category: creative-arts
field: graphic-design
product: poster-and-campaign-graphics
tags: [graphic-design, poster-and-campaign-graphics, figma-auto-layout, figma-components, figma-variants, campaign-adaptation, resizing, responsive-layout]
level: practitioner
status: draft
description: "Adapt one campaign layout to many formats in Figma using auto layout, resizing rules, components with variants, and variables for colour and copy."
sources:
  - https://help.figma.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Campaign adaptations with Figma auto layout and components

**Goal:** one master layout that produces banner, story, square and print variants with little manual rework.

## Setup
1. Create one **frame** per format (for example 1080x1080, 1080x1920, 1200x628, 728x90) from the frame tool presets or by typing W and H.
2. Build the shared content as **components**: logo, headline block, CTA button, image slot.

## Auto layout
- Select layers and press **Shift+A** to wrap them in an auto layout frame (or use the Auto layout control in the right panel).
- Set direction (horizontal or vertical), gap, and padding.
- Per-child resizing: **Hug contents**, **Fill container**, or **Fixed**. Typical pattern: container Fixed to the format size; the text block Fill container so it reflows; the button Hug.
- Use **min and max width** on text blocks so copy does not stretch too wide in wide formats.
- Use **constraints** for children of normal frames; use **Absolute position** inside an auto layout frame for a badge or logo that must pin to a corner.

## Components and variants
- Make the CTA and headline blocks components, then add **variants** with properties such as Size (S/M/L) and Theme (light/dark). Use **component properties** (text, boolean, instance swap) to change copy or hide a secondary line without detaching.
- Keep source components in a library file so edits propagate to every adaptation.

## Variables
Define colour variables (brand, background, text) and, if useful, string variables for copy, with modes for light/dark or per-campaign themes. Switching the mode on a frame re-themes it.

## Export
Use the **Export** section on the frame: PNG or JPG at 1x or 2x for digital, SVG or PDF for vector. Name frames with the final file name so exports arrive labelled.

## Failure modes
- Detaching instances to patch one format, which breaks updates; add a variant or property instead.
- Hard-coded text sizes in banners; verify minimum legible size in the smallest format.

## Self-check
Change the headline in the master; every format updates and nothing overflows. Review the smallest and tallest formats first.
