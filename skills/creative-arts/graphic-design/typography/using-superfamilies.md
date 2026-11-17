---
id: creative-arts.graphic-design.typography.using-superfamilies
name: using-superfamilies
category: creative-arts
field: graphic-design
product: typography
tags: [graphic-design, typography, typeface-selection, font-pairing, superfamily, type-system, serif-and-sans-family, weights-and-widths, brand-type-system, variable-font-families]
level: practitioner
status: draft
description: "Build typographic systems from superfamilies (serif, sans, mono and widths designed together): when to use them, choosing members by role, and avoiding too many weights."
sources:
  - https://fonts.adobe.com/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Using superfamilies

**Goal:** a complete, harmonious type system from one design family - many voices, one personality.

## What a superfamily is
A family designed with several related sub-families sharing proportions, x-height and details: e.g. **serif + sans**
(Thesis/TheSans/TheSerif, Scala/Scala Sans, Source Serif/Sans/Code, IBM Plex Sans/Serif/Mono, Noto), plus widths
(condensed, extended), weights, optical sizes, sometimes slab and mono (Lupton: families vs superfamilies).

## When to use
- Complex documents and brands needing many levels (reports, wayfinding, publications, UI + marketing) - serif for
  long reading, sans for navigation and data, mono for code - all in visual harmony.
- Multilingual work: superfamilies like Noto or Plex extend to many scripts with matched design.
- Teams without strong typographic judgment: built-in harmony reduces pairing mistakes.

## Building the system
1. Assign roles by sub-family: Serif Text for body, Sans for headings/UI, Sans Condensed for tables/charts, Mono for code.
2. Choose **few weights** per role (e.g. Regular, Italic, Semibold, Bold) - variety comes from sub-families, not from
   every weight. Two weights apart for clear contrast (Regular vs Semibold/Bold, not Regular vs Medium).
3. Define styles (paragraph/character styles, CSS tokens) per role (see UI type tokens skill).
4. Variable font versions let you fine-tune weight/width/opsz while keeping files few (see variable fonts).

## Gotchas
- A superfamily can feel flat if contrast is too subtle; use size, weight and space for hierarchy too.
- Licensing: sub-families are often sold separately; budget for all roles across all media.
- Do not mix in a third unrelated family without a clear role.

## Verify
- [ ] Every role mapped to a sub-family and limited weights; styles defined.
- [ ] Licences cover all sub-families and media used.
