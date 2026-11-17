---
id: creative-arts.design-for-form-and-experience.figma.organising-figma-pages-with-sections
name: organising-figma-pages-with-sections
category: creative-arts
field: design-for-form-and-experience
product: figma
tags: [figma-sections, sections, figma-pages, file-organization, dev-mode-ready, file-structure, figma]
level: practitioner
status: draft
description: "Organise Figma files with pages and sections: structure by status or flow, name consistently, use section fills and Ready for dev markers, and keep the file performant."
sources:
  - "Figma Help Center - Sections (help.figma.com/hc/en-us/articles/10526209131287)"
  - "Figma Help Center - Pages and file organisation (help.figma.com)"
  - "Figma Dev Mode - Mark designs ready for dev (help.figma.com/hc/en-us/articles/15023124644247)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Pages and sections

## Pages (top level)
Typical file: **Cover** (thumbnail, status, owner), **Read me** (purpose, links, changelog), **Components** (library), **Flows** or per-feature pages, **Explorations** (WIP), **Archive**. Prefix with emoji or numbers for sort and status (checks for "Ready"). One page per major flow keeps rendering fast; very large pages slow the canvas.

## Sections (**Shift+S**)
- A **section** is a labelled container on the canvas for frames; it moves its frames and shows a **title** and optional **fill colour**. Sections cannot be nested inside other sections, but frames and sections can be dragged and the layer panel shows hierarchy.
- Use **one section per flow or status**: "Onboarding - Ready for dev", "Checkout - In review", "Explorations".
- Use the **Ready for dev** status on sections or frames to tell developers what is final in Dev Mode.
- Section fill colours: use a consistent code (grey draft, blue review, green approved); add a **description** in the section name or sticky.
- Flow arrangement: frames left to right in reading order, with **prototype flow starting points** at the first frame and a **flow name** (`creative-arts.design-for-form-and-experience.figma.prototype-triggers-actions-and-flows`).

## Naming and hygiene
- Frame naming: `Flow / Screen / State` (e.g. `Checkout / Payment / Error`); component naming with slashes (`Button/Primary/Large`).
- Remove hidden or unused layers, outlines, and off-canvas debris; flatten complex vectors only when needed.
- Keep large images out or compressed; split big libraries into several files; use the **Assets** panel and library for reuse.
- Add **comments** or sticky notes for decisions; keep **Version history** milestones for releases (`creative-arts.design-for-form-and-experience.figma.comments-and-version-history`).
- Share a **file template** for teams.

## Verify
- [ ] Cover, Read me and Components pages exist; page names consistent.
- [ ] Flows are in labelled sections with status colours.
- [ ] Layers named; file stays responsive.
