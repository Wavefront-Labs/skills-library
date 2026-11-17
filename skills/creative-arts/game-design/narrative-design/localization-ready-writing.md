---
id: creative-arts.game-design.narrative-design.localization-ready-writing
name: localization-ready-writing
category: creative-arts
field: game-design
product: narrative-design
tags: [game-design, narrative-design, localization-writing, localisation, l10n, internationalization, string-tables, translator-notes]
level: practitioner
status: draft
description: "Write game text that localises cleanly: no string concatenation, ICU plurals and gender, length budgets for expansion, translator context notes and pseudolocalisation checks."
sources:
  - https://unicode-org.github.io/icu/userguide/format_parse/messages/
  - https://cldr.unicode.org/index/cldr-spec/plural-rules
  - https://igda.org/sigs/localization/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Localisation-ready writing

**Goal:** text that translators can render naturally in every target language without
engineering changes or broken grammar.

## Rules for writers
1. **Never build sentences from fragments.** `"You found " + count + " " + item` cannot
   be translated; word order and agreement differ by language. Write whole sentences with
   named placeholders: `"You found {count} {item}."`
2. **Use ICU MessageFormat for plurals and gender:**
   ```
   {count, plural, one {You found # coin.} other {You found # coins.}}
   {gender, select, female {She is ready.} male {He is ready.} other {They are ready.}}
   ```
   CLDR plural categories differ: English has one/other, Russian one/few/many/other,
   Arabic zero/one/two/few/many/other, Japanese only other.
3. **Budget for expansion:** German and French run ~30% longer than English on average,
   and short strings can double or triple. Give UI strings a max length and design the
   widget for +40%.
4. **Write translator notes** per string: who speaks, to whom, tone, what the placeholder
   holds, max length, whether it is a pun or reference. "Fire" as verb vs noun is the classic trap.
5. **Avoid untranslatable devices** or flag them: puns, rhymes, alliteration, wordplay in
   puzzle answers, culture-specific idioms. Puzzles depending on English letters need a design solution.
6. **One string, one meaning:** do not reuse "Open" for both a menu verb and a door state.
7. **No text in textures**; if unavoidable, list them for re-authoring.

## String table hygiene
- Stable, descriptive keys (`quest.mill_02.objective.find_daughter`), never the English text as key.
- Columns: key, source text, context note, speaker, max length, VO id, status.
- Freeze source text before sending; every change after triggers retranslation and re-recording.

## Pseudolocalisation test
Replace text with accented, padded variants (`[Ŷöû ƒöûñð ŧĥê ķêý!!!!]`) to reveal hardcoded
strings, truncation and font gaps before real translation starts.

## Gotchas
- Gendered languages need speaker and listener gender for player-character lines.
- Dates, numbers and currencies through locale formatters, not hand-formatted.
- CJK and Arabic need fonts with full glyph coverage and right-to-left layout for Arabic and Hebrew.

## Verify
- [ ] Zero concatenated sentences in the string table.
- [ ] Every placeholder string has a context note.
- [ ] Pseudolocalised build shows no untranslated or clipped strings.
