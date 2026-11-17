---
id: languages-linguistics.writing-systems-and-scripts.orthography-design.designing-a-practical-orthography
name: designing-a-practical-orthography
category: languages-linguistics
field: writing-systems-and-scripts
product: orthography-design
tags: [orthography-design, orthography, practical-orthography, spelling-system, grapheme-phoneme-mapping, phonemic-orthography, phoneme-inventory, digraphs, diacritics, tone-marking, script-choice, unwritten-languages, endangered-languages, language-documentation, community-orthography, spelling-reform, word-breaks, keyboard-layout, unicode, sil, literacy-materials, orthography-testing]
level: advanced
status: draft
description: "Design or reform a writing system for a language: phonemic analysis, grapheme choices, tone and word-break decisions, typeability, community testing and the sociolinguistic trade-offs."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Designing a practical orthography

**Goal:** produce a spelling system that speakers can learn quickly, read fluently,
type on everyday devices and accept as theirs — for a previously unwritten language, or
to reform an existing one.

> Draft. Synthesised from field-linguistics and language-development practice (e.g. the
> orthography-design literature associated with SIL and documentary linguistics) as
> generally described. Community acceptance is the deciding factor; linguistic elegance
> isn't.

## 1. Linguistic groundwork
1. **Phoneme inventory:** establish contrasts with minimal pairs, including length, tone,
   nasalisation, stress if contrastive. Orthographies should usually be **phonemic**, not
   phonetic: write the contrasts, not predictable allophones.
2. **Morphophonemics:** decide whether to spell a morpheme the same everywhere
   (morphophonemic, easier for fluent readers to recognise words) or as pronounced
   (phonemic surface, easier for beginners). Many successful orthographies compromise.
3. **Functional load:** a contrast distinguishing many common words must be written;
   one distinguishing two rare words may be left unmarked (often the debate over tone).
4. **Dialect survey:** which variety is the base? Can the spelling cover several dialects
   by writing the more conservative form?

## 2. Script and grapheme choices
- **Script:** usually the script of the region's dominant/school language, so readers
  transfer skills and keyboards exist. Religious, political and identity factors can
  override this — and should be heard.
- **Map the familiar first:** sounds shared with the language of wider communication
  use its letters with its values. Avoid giving a familiar letter an unfamiliar sound
  unless the community wants it.
- **Extra phonemes:** options are digraphs (ng, sh), diacritics (ñ, ẽ), or special letters
  (ŋ, ɛ, ɔ). Trade-offs: digraphs type easily but lengthen words and can be ambiguous
  (is "ng" /ŋ/ or /n+g/?); special letters are precise but need keyboards and fonts;
  diacritics get dropped in casual typing.
- **Tone:** mark fully, mark only where ambiguous (grammatical tone, minimal pairs), or
  not at all. Test readers both ways; heavy tone marking often slows fluent readers while
  unmarked tone can block beginners.

## 3. Practical constraints
- **Unicode:** every character must exist in Unicode; prefer precomposed characters where
  they exist and check combining sequences render in common fonts.
- **Typing:** design or adopt keyboard layouts for phones and computers (Keyman is a
  common tool). If people can't text in it, they'll invent their own spelling.
- **Capitalisation, punctuation, word breaks:** decide clitics and affixes — joined,
  hyphenated, or separate — and write it down with examples.
- **Sorting order** for dictionaries.

## 4. Testing with the community
1. Draft with a group of speakers (teachers, elders, young people), not alone.
2. **Reading tests:** have new readers read unfamiliar texts; count hesitations and
   misreadings per feature (tone marks, digraphs).
3. **Writing tests:** dictate text; see which spellings vary — variation points to rules
   that are unclear or unlearnable.
4. Revise, then **pilot** in real materials (primers, story books, signage) for a period
   before declaring it standard.
5. Document the result: an orthography statement with the grapheme–phoneme table,
   rules, examples and rationale.

## 5. Reform-specific cautions
Changing an existing orthography strands old texts and literate adults; benefits must
clearly beat that cost. Phase changes, provide converters, and expect resistance tied to
identity.

## Gotchas
- Writing allophones → too many symbols.
- Choosing IPA symbols because they're "correct", then nobody can type them.
- Ignoring how people already write informally on phones — it's evidence.
- One outside linguist deciding; adoption fails.

## Verify
- [ ] Every phonemic contrast with real functional load has a written representation.
- [ ] All characters are in Unicode and typeable on a phone keyboard you've tested.
- [ ] New readers' error rates on test texts are documented per feature.
- [ ] A written orthography statement exists with examples and word-break rules.
- [ ] Community representatives have formally agreed the draft.
