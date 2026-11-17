---
id: computing-software.web-development.web-accessibility.text-spacing-overrides
name: text-spacing-overrides
category: computing-software
field: web-development
product: web-accessibility
tags: [distinguishable, text-spacing, wcag-1-4-12, typography, css]
level: practitioner
status: verified
description: "Meeting WCAG 1.4.12 Text Spacing: surviving user overrides of line height, paragraph, letter and word spacing without clipping or overlap, plus the test bookmarklet."
sources:
  - https://www.w3.org/WAI/WCAG22/Understanding/text-spacing.html
  - https://dylanb.github.io/bookmarklets.html
  - https://www.w3.org/WAI/WCAG22/Techniques/failures/F104
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Text spacing overrides

**1.4.12 (AA):** no loss of content or functionality when users set:
- line height to at least **1.5** times the font size,
- spacing after paragraphs to **2** times the font size,
- letter spacing to **0.12** times the font size,
- word spacing to **0.16** times the font size.
People with dyslexia and low vision apply these through extensions or user stylesheets. You don't have to provide controls - just not break.

## 1. Test stylesheet
```css
* { line-height: 1.5 !important; letter-spacing: .12em !important; word-spacing: .16em !important; }
p { margin-bottom: 2em !important; }
```
(The "Text spacing" bookmarklet at dylanb.github.io/bookmarklets.html sets the same four values inline with `!important`: `p` margin-bottom 2em, line-height 1.5, letter-spacing 0.12em, word-spacing 0.16em.) Run here: a 90x20 `overflow:hidden` `white-space:nowrap` label needed 100x24 inside a 90x20 box (clipped), while a wrapping `min-height` box simply grew to 48px tall.

## 2. What breaks
- Fixed `height` on buttons, badges, cards, nav items with `overflow: hidden` -> text clipped.
- Labels/text absolutely positioned over images or other text -> overlap.
- Truncation with `white-space: nowrap; text-overflow: ellipsis` hiding essential words.
- Icon fonts and custom toggles sized by line height.
- Text inside SVG with fixed dimensions; canvas-drawn text.
- Tabs and segmented controls that overflow their container without wrapping or scrolling.

## 3. Fixes
- `min-height` instead of `height`; padding instead of fixed line boxes.
- Let containers grow; allow wrapping (`flex-wrap`, no `nowrap` on labels).
- Use `em`-based spacing so components scale with text.
- For unavoidable truncation, provide the full text another way (expand, tooltip on focus, detail view).

## 4. Scope
Applies to HTML/CSS text you control. Text in images and captions burned into video aren't covered (other criteria apply), and languages/scripts that don't use a property are exempt from it.

## Verify
Apply the bookmarklet on each template at desktop and mobile widths; screenshot compare before/after for clipped or overlapping text.
