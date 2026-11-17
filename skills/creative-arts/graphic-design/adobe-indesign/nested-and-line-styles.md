---
id: creative-arts.graphic-design.adobe-indesign.nested-and-line-styles
name: nested-and-line-styles
category: creative-arts
field: graphic-design
product: adobe-indesign
tags: [graphic-design, adobe-indesign, indesign, paragraph-styles, character-styles, nested-styles, nested-line-styles, drop-caps, run-in-lead-ins, end-nested-style-here, automation]
level: practitioner
status: draft
description: "Automate character formatting inside InDesign paragraphs with nested styles (up to a character, word count, tab) and nested line styles, including drop caps and run-in heads."
sources:
  - https://helpx.adobe.com/indesign/using/drop-caps-nested-styles.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Nested and line styles

**Goal:** formatting that applies itself: bold lead-ins, small-cap first lines, styled numbers - without selecting text by hand.

## Nested styles (Paragraph Style Options > Drop Caps and Nested Styles)
A sequence of rules: apply character style X **through/up to** N of something.
- Examples of "something": Sentences, Words, Characters, Letters, Digits, **Tab Characters**, Forced Line Break,
  Em Space, En Space, Anchored Object Marker, Inline Graphic, **End Nested Style Character**, or any typed character (e.g. `:` or `.`).
- **Run-in head:** `Bold` **through 1** `.` - everything up to and including the first full stop is bold.
- Directory listing: `Name` up to 1 Tab Character, then `Phone` up to 1 Tab Character.
- **Repeat** rule loops previous rules (alternating styles in a list).
- Insert **End Nested Style Here** (Type > Insert Special Character > Other) where you want a rule to stop in
  awkward cases.

## Nested line styles
Same dialog, lower section: apply character style X **for N lines** - e.g. first line of each article in small caps
(`Small caps` for 1 Lines). Recalculates as text reflows - impossible by hand.

## Drop caps
Lines (e.g. 3) and Characters (1); apply a character style to the drop cap (different typeface/colour);
**Align Left Edge** and **Scale for Descenders** options. Use in an opener paragraph style (`Body First Drop`).
Optical adjustment: kern after the drop cap (place cursor after it, Alt/Option+arrows), or use a hair space.

## Combine with GREP styles
Nested styles work by position; GREP styles by pattern (see GREP styles skill). Both can live in one paragraph style.

## Gotchas
- Character styles used in nested styles should define only what changes (e.g. just weight), so they work on any base font.
- A nested style counting "Words" counts punctuation-separated chunks in unexpected ways - test with real copy.
- Drop caps with quotes (`"A`) need 2 characters or a hanging adjustment.

## Verify
- [ ] Editing copy keeps lead-ins and first lines correctly formatted.
- [ ] No manual character formatting where a nested rule exists.
