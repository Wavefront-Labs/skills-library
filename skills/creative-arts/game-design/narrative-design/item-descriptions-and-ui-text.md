---
id: creative-arts.game-design.narrative-design.item-descriptions-and-ui-text
name: item-descriptions-and-ui-text
category: creative-arts
field: game-design
product: narrative-design
tags: [game-design, narrative-design, ui-text, item-descriptions, ux-writing, microcopy, tooltips, flavour-text]
level: practitioner
status: draft
description: "Write item descriptions and UI text: function-first tooltips, flavour lines that carry lore, consistent terminology, button labels and error messages players read."
sources:
  - https://www.nngroup.com/articles/ten-usability-heuristics/
  - https://www.routledge.com/The-Game-Narrative-Toolbox/Heussner-Finley-Hepler-Lemay/p/book/9781138778382
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Item descriptions and UI text

**Goal:** text players can scan in under two seconds that tells them what to do, and
flavour that rewards those who read further.

## Item description template
```
Ember Blade                      <- name: unique, evokes function or origin
Sword  ·  Rare                   <- type and rarity
+12 Fire damage on hit           <- mechanics: numbers, in standard terms, first
Ignites oil-soaked enemies.      <- interaction rule in one line
"Forged where the old kiln fell." <- flavour: italic, one or two lines, last
```
- **Function before flavour**, always visually separated.
- Mechanics text uses the game's glossary words exactly ("Fire damage", not "burn" here
  and "flame" there). Keep a terminology list and lint against it.
- Dark Souls-style lore-in-items works because each line implies a story; one concrete
  detail beats a paragraph of history.

## UI text rules
1. **Buttons are verbs**: "Equip", "Sell all junk", not "OK".
2. **Confirmations name the consequence**: "Sell Ember Blade for 120 gold? You cannot buy it back."
3. **Errors say what to do next**: "Inventory full. Drop or sell an item to pick this up."
4. **Sentence case**, consistent across the game; decide once.
5. **Numbers as numerals**, units consistent (s, %, m).
6. **Tooltips** answer "what does this do" and "why can't I use it" (greyed-out reasons).

## Process
- UI text lives in the string table with keys and length limits (see localisation-ready writing).
- Review text in-context in the build, not in a spreadsheet; truncation and tone show only there.
- Playtest: ask players to explain an item from its tooltip; misreads are bugs.

## Gotchas
- Stat text generated from data drifts from flavour; generate the mechanics line from the
  same data the game uses.
- Jokes in error messages age badly on the tenth view.
- Colour alone to show rarity or stat up/down fails colour-blind players; add icon or text.

## Verify
- [ ] Every item has mechanics line generated from data, plus optional flavour.
- [ ] Terminology list exists and all UI text conforms.
- [ ] Every disabled action has a reason tooltip.
