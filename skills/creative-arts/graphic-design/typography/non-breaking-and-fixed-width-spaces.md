---
id: creative-arts.graphic-design.typography.non-breaking-and-fixed-width-spaces
name: non-breaking-and-fixed-width-spaces
category: creative-arts
field: graphic-design
product: typography
tags: [graphic-design, typography, typographic-details, punctuation, non-breaking-space, thin-space, hair-space, em-space, en-space, figure-space, narrow-no-break-space, white-space-characters]
level: practitioner
status: draft
description: "Use special spaces correctly: non-breaking spaces to bind values and units or names, thin and hair spaces for fine spacing, em/en/figure spaces, and French narrow no-break spaces."
sources:
  - https://helpx.adobe.com/indesign/using/glyphs-special-characters.html
  - https://www.unicode.org/charts/PDF/U2000.pdf
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Non-breaking and fixed-width spaces

**Goal:** spaces that never break where they should not and have exactly the width the typography needs.

## The spaces (InDesign: Type > Insert White Space)
| Space | Width | Use | InDesign Find/Change code |
|---|---|---|---|
| **Non-breaking space** | flexible (like a word space) | `10 kg`, `p. 12`, `Mr Smith`, `Henry VIII` | `^S` (`~S` in GREP) |
| Non-breaking (fixed width) | fixed | same, when justification must not stretch it | `^s` |
| **Em space** | 1 em | separating run-in heads, indents | `^m` |
| **En space** | 1/2 em | between list numbers and text in some styles | `^>` |
| **Thin space** | 1/8 em (InDesign) | around em dashes, between initials (J. R. R.), before %, in French punctuation | `^<` |
| **Hair space** | 1/24 em | tiny optical adjustments (quote marks, dashes) | `^\|` |
| **Figure space** | width of a tabular digit | aligning numbers in lists without tabs | `^/` |
| Punctuation space | width of a full stop | aligning decimals | `^.` |
| Flush space | variable | fills last line of justified text before an end mark | `^f` |
Unicode equivalents: no-break U+00A0, narrow no-break U+202F, thin U+2009, hair U+200A, figure U+2007, em U+2003, en U+2002.

## Typical rules
- Bind numbers to units and symbols (`25 %` in European styles, `5 km`), dates (`12 March`), titles to names, and the
  last two words of a headline if needed.
- **French:** a narrow no-break space before `; : ! ?` and inside « guillemets ». Set the Language to French and
  InDesign can add them automatically in some versions; otherwise Find/Change.
- Thousands separators in some styles are thin spaces (`1 000 000`, SI style) - use the narrow no-break space so
  numbers never split.

## Cleanup
- Double spaces: Find `  +` (two or more spaces, GREP ` {2,}`) change to single space.
- Spaces used for alignment: replace with tabs or proper indents.
- Web: `&nbsp;` for non-breaking, `&thinsp;`, `&#8239;` (narrow no-break).

## Verify
- [ ] Type > Show Hidden Characters: no double spaces, no space-based alignment.
- [ ] Values and units never split across lines; French punctuation spaced correctly.
