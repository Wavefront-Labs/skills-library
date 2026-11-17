---
id: creative-arts.graphic-design.typography.headings-subheads-and-run-in-heads
name: headings-subheads-and-run-in-heads
category: creative-arts
field: graphic-design
product: typography
tags: [graphic-design, typography, type-hierarchy, headings, subheads, run-in-heads, crossheads, side-heads, heading-levels, space-above-below, keep-with-next, nested-styles]
level: practitioner
status: draft
description: "Design a heading system: levels A to D, displayed vs run-in heads, space above and below on the baseline grid, keep options, and how to style each level with one change."
sources:
  - https://helpx.adobe.com/indesign/using/drop-caps-nested-styles.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Headings, subheads and run-in heads

**Goal:** a heading hierarchy readers decode without thinking, and that the layout can set
automatically from styles.

## Count the levels first
- Ask the editor for the real structure: most non-fiction needs 2-3 heading levels (A, B, C); more than 4
  usually signals structural problems in the text, not a typography problem.
- Name styles by level (`H-A`, `H-B`, `H-C-runin`), not by look.

## Heading forms (Bringhurst, Lupton)
- **Displayed heads:** on their own line. Options: centred, flush left, hanging into the margin (side heads).
- **Run-in heads:** start the paragraph in bold, small caps or italic, followed by a full stop, em space or
  colon, then text continues: `**Choosing paper.** The first decision...`. Ideal for the lowest level:
  saves space and keeps rhythm.
- **Crossheads** (newspapers and magazines): short heads breaking long text, often centred or in a
  contrasting sans.

## Spacing on the baseline grid
- Total space taken by a heading (space above + heading lines + space below) should equal a whole number of
  body lines, so text after it returns to the grid. E.g. body 10/13: H-B is 13 pt bold with 13 pt space
  above, 0 below = two lines.
- More space above than below binds the heading to its text.
- Keep Options: **Keep with Next 2 lines**; avoid a heading as the last line of a column.

## Distinguish levels with one or two variables
- A: size + weight; B: weight only at text size; C: italic or small caps run-in. Same face throughout is
  usually stronger than a second family.
- Numbered heads (1.2.3) for technical documents: use InDesign paragraph numbering, not typed numbers.

## Run-in heads in InDesign
- Use a **nested style**: character style `run-in-bold` through 1 `.` or through the first em space;
  or in CSS a `<strong>` inside the paragraph, or `display: run-in` (not supported, so use inline markup).

## Gotchas
- Headings set in all caps cannot be long; edit them or switch to sentence case.
- Underlined headings, colour-only differences and too many sizes create noise.
- Widowed headings at column bottom: fix with keep options, not manual returns.

## Verify
- [ ] Heading levels are identifiable when the layout is blurred (squint test).
- [ ] Body text after every heading sits on the baseline grid.
