---
id: creative-arts.graphic-design.adobe-indesign.grep-styles
name: grep-styles
category: creative-arts
field: graphic-design
product: adobe-indesign
tags: [graphic-design, adobe-indesign, indesign, paragraph-styles, character-styles, grep-styles, grep, regular-expressions, no-break, widow-control, automatic-formatting]
level: advanced
status: draft
description: "Apply character styles automatically by pattern with InDesign GREP styles: prices, units, phone numbers, acronyms in small caps, no-break rules and short-last-line fixes."
sources:
  - https://helpx.adobe.com/indesign/using/drop-caps-nested-styles.html
  - https://helpx.adobe.com/indesign/using/metacharacters-searching.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# GREP styles

**Goal:** formatting rules that keep working as text is edited - every price bold, every acronym in small caps, no number split from its unit.

## Where
Paragraph Style Options > **GREP Style** > New GREP Style: choose a character style and type the expression.
Applies live to every paragraph in that style.

## Useful patterns
| Purpose | GREP | Character style |
|---|---|---|
| Prices | `[$£€]\d+(?:[.,]\d{2})?` | Bold |
| Acronyms 2+ capitals | `\b\u{2,}\b` | Small caps (all small caps or OpenType `c2sc`) |
| Keep number + unit together | `\d+\s(?:mm\|cm\|kg\|%)` (escape the pipe only in this table) | No Break |
| Keep last two words together (avoid one-word last lines) | `\S+\s\S+$` or `(?<=\s)\S+\s\S+$` | No Break |
| Phone numbers | `\+?\d[\d ]{7,}\d` | No Break |
| Ordinals superscript | `(?<=\d)(st\|nd\|rd\|th)\b` | Superscript |
| Text in brackets | `\(.+?\)` | Italic or colour |
| Web URLs | `(?i)https?://\S+` | Link colour |
Create a `No Break` character style with only the No Break attribute set.

## Writing and testing
- Test expressions in Edit > Find/Change > **GREP** tab first; Find Next shows what matches.
- Use lookbehind `(?<=...)` and lookahead `(?=...)` to style only part of a match.
- `\b` word boundary, `\d` digit, `\u` uppercase, `\l` lowercase, `+?` lazy.
- Save tested queries in Find/Change (disk icon) for reuse.

## Gotchas
- Nested styles are applied first, then GREP styles; where both touch the same text, the GREP style's
  attributes win. Test combinations on real copy.
- Heavy GREP styles on very long documents slow composition; keep patterns specific.
- A No Break rule matching too much text causes overset or awful spacing - keep ranges short.

## Verify
- [ ] Each pattern tested in Find/Change; real copy edits keep formatting.
- [ ] No overset caused by No Break rules; acronyms and units render as intended.
