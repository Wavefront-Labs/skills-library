---
id: creative-arts.graphic-design.typography.hyphenation-and-justification-settings
name: hyphenation-and-justification-settings
category: creative-arts
field: graphic-design
product: typography
tags: [graphic-design, typography, justification, text-alignment, hyphenation-and-justification, h-and-j, word-spacing, letter-spacing, glyph-scaling, hyphenation-zone, rivers, indesign, justified-text]
level: practitioner
status: draft
description: "Set justified text without rivers: InDesign word spacing, letterspacing, glyph scaling and hyphenation limits, H&J violation highlighting and line fixes."
sources:
  - https://helpx.adobe.com/indesign/using/text-composition.html
  - https://helpx.adobe.com/indesign/using/hyphenation-justification.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Hyphenation and justification (H&J) settings

**Goal:** justified columns with even texture: no rivers, no gappy lines, few consecutive hyphens.

## When to justify
Justify only when the measure is wide enough: roughly **40+ characters per line**. Narrower
columns (newspaper, captions) justify badly - set them ragged right.

## Justification (Paragraph panel menu > Justification), body text starting values
| | Minimum | Desired | Maximum |
|---|---|---|---|
| Word Spacing | 80% | 100% | 133% |
| Letter Spacing | -2% | 0% | 2% |
| Glyph Scaling | 98% | 100% | 102% |
- Tighter word spacing range = more even texture but more hyphenation needed.
- Glyph scaling beyond +/-3% visibly distorts letters; many typographers allow 0 or +/-2%.
- **Composer: Adobe Paragraph Composer** (considers the whole paragraph; much better than
  single-line). See the paragraph composer skill.
- Single Word Justification: Align Left (avoids a single stretched word on its own line).

## Hyphenation (Paragraph panel menu > Hyphenation)
- Words with at least **6** letters; After First **3**; Before Last **3** (2 is acceptable in narrow columns).
- **Hyphen Limit: 2-3** consecutive hyphens.
- **Hyphenation Zone** (ragged text only): larger = fewer hyphens, rougher rag.
- Slider "Better Spacing <-> Fewer Hyphens": middle is fine for justified body text.
- Hyphenate Capitalized Words: off. Hyphenate Last Word: off. Hyphenate Across Column: off.
- Set the correct **Language** in the Character panel: hyphenation dictionaries are per language.

## Show the problems
Preferences > Composition > **Highlight H&J Violations**: yellow shading on lines exceeding
your limits (darker = worse). Also Highlight Keep Violations.

## Fixing a bad line (in order)
1. Edit the copy if you can (writers often will).
2. Adjust tracking on the whole paragraph by -5 to +5 (never more on body text).
3. Add a discretionary hyphen (Ctrl/Cmd+Shift+-) or No Break on two words.
4. Accept it - better than a distorted line.

## Gotchas
- Rivers (vertical channels of white) come from large word spaces lining up: check by
  squinting at the page upside down.
- Different settings across body styles make texture inconsistent: set H&J in the base Body style.

## Verify
- [ ] Highlight H&J Violations shows only light yellow, no dark lines.
- [ ] No more than 2-3 consecutive hyphens; no rivers at arm's length.
