---
id: creative-arts.comics-and-sequential-art.lettering.crossbar-i-and-alternate-glyphs
name: crossbar-i-and-alternate-glyphs
category: creative-arts
field: comics-and-sequential-art
product: lettering
tags: [lettering, lettering-fonts, comic-fonts, crossbar-i, alternate-glyphs, opentype-alternates, contextual-alternates, glyphs-panel]
level: practitioner
status: draft
description: "Apply the crossbar I rule (serifed I only for the pronoun and acronyms/initials) and use OpenType alternates in comic fonts so repeated letters don't look mechanical."
sources:
  - https://blambot.com/pages/comic-book-grammar-tradition
  - https://www.comicbookfonts.com/
  - https://helpx.adobe.com/illustrator/using/special-characters.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Crossbar I and alternate glyphs

**Goal:** correct traditional I usage and natural-looking lettering.

## The crossbar I rule (Blambot grammar and widespread tradition)
- Use the **I with crossbars (serifs)** for:
  - the personal pronoun **I** and its contractions (I'M, I'LL, I'D, I'VE);
  - acronyms/initialisms and initials where the letter stands alone (e.g. in some
    styles, letters in "C.I.A.").
- Use the **plain vertical-stroke I** everywhere else, inside words (THIS, BIG).
Why: in all caps, a plain-stroke I standing alone can look like a "1" or "l".

## How fonts implement it
- Many comic fonts map the crossbar I to the **capital I** key and the plain I to the
  **lowercase i** key, so typing "I like it" in sentence case gives correct output in
  an all-caps font. Others use OpenType contextual alternates that switch
  automatically. **Read the font's manual**; behaviour varies.
- Typing the script in all caps can break this mapping (every I becomes crossbar).
  Paste in sentence case or fix with find/replace.

## Alternates for natural rhythm
- Some fonts include alternate letterforms and automatic contextual alternates so
  double letters (LL, OO, EE) don't look identical. Enable OpenType Contextual
  Alternates in Illustrator (OpenType panel) or the app's equivalent.
- The Glyphs panel (Illustrator: Type > Glyphs) inserts specific alternates manually.

## Check
- Search lettered text for " I " and contractions; confirm crossbar form.
- Spot-check words containing I for plain form.

## Verify
- [ ] Pronoun I and contractions use crossbar I everywhere.
- [ ] Plain I inside words.
- [ ] Contextual alternates on if the font supports them.
