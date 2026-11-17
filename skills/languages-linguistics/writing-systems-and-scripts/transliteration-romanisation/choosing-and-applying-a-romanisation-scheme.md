---
id: languages-linguistics.writing-systems-and-scripts.transliteration-romanisation.choosing-and-applying-a-romanisation-scheme
name: choosing-and-applying-a-romanisation-scheme
category: languages-linguistics
field: writing-systems-and-scripts
product: transliteration-romanisation
tags: [transliteration-romanisation, romanization, transliteration, transcription, pinyin, hanyu-pinyin, wade-giles, hepburn, kunrei-shiki, revised-romanization, mccune-reischauer, iso-9, gost, bgn-pcgn, ala-lc, iast, iso-15919, din-31635, unicode, diacritics, reversible-transliteration, icu-transform, catalog-romanization, passport-names, place-names]
level: practitioner
status: docs-checked
description: "Pick the right romanisation scheme for the job (ALA-LC for catalogues, BGN/PCGN for place names, others) and apply it consistently: reversibility, diacritics, names and tooling."
sources: [https://www.loc.gov/catdir/cpso/roman.html, https://www.gov.uk/government/publications/romanisation-systems/russian-romanization-april-2019, https://www.unicode.org/reports/tr15/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Choosing and applying a romanisation scheme

**Goal:** convert names and text from a non-Latin script into Latin letters in a way that
fits the purpose — readable, standard, or reversible — and do it consistently.

> For any catalogue, legal or cartographic job, apply the official table, not this summary.

## 1. Decide the purpose first
- **Transliteration** maps **graphemes**: each source character has a defined Latin
  equivalent, ideally reversible. Good for libraries, data, citations.
- **Transcription** maps **sounds**: helps readers pronounce it (most "popular" schemes).
- Most real schemes mix both. Ask: *Who reads this? Must it be reversible? Is there an
  official or established form already?*

## 2. Where the official tables live
- **Library catalogues:** the ALA-LC romanization tables (approved by the Library of
  Congress and the American Library Association) cover, among others, Arabic-script
  languages, Russian and other Cyrillic-script languages (separate tables for Belarusian,
  Bulgarian, Macedonian, Serbian, Ukrainian and more), Chinese, Japanese, Korean, Greek and
  Sanskrit/Prakrit. Note the edition year of each table.
- **Geographic names, Russian:** the BGN/PCGN system, jointly agreed by the US Board on
  Geographic Names and the UK Permanent Committee on Geographical Names; the UK Ministry
  of Defence publishes the Russian table on gov.uk.
- **Other uses** (Hanyu Pinyin, Hepburn or Kunrei-shiki, Revised Romanization or
  McCune–Reischauer, ISO 9, IAST, ISO 15919, DIN 31635): choose by the audience, then take
  the table and edition from the scheme's own publisher.

## 3. Applying it consistently
1. **Write a mini style sheet:** scheme + edition, diacritics yes/no, capitalisation and
   word-division rules, exceptions list.
2. **Exceptions for established forms:** well-known names keep their conventional
   spellings. Personal names: use the person's own preferred romanisation when known.
3. **Word division** is a real decision in several schemes; follow the scheme's rules.
4. **Diacritics** must be real Unicode characters; normalise to NFC (canonical
   decomposition followed by canonical composition, per Unicode UAX #15).

## 4. Tooling
- ICU transliterators are available in many languages via ICU bindings; check the
  transform matches your scheme. A generic any-script-to-Latin transform is not an
  official standard.
- Automatic converters make errors on ambiguous readings (polyphonic characters, kanji
  names, sound-change rules) — **review output by hand**.
- Spreadsheet: keep source, romanised, scheme, and "checked by" columns.

## Gotchas
- Mixing schemes in one document (Peking and Beijing; Tchaikovsky and Chaykovskiy).
- Stripping diacritics from a scheme that needs them for reversibility.
- Romanising Japanese kanji names automatically — readings are ambiguous; ask or source.
- Assuming "Cyrillic" means one scheme: ALA-LC publishes separate tables per language.
- Apostrophes and primes in some schemes break naive search; plan a stripped search key.

## Verify
- [ ] The scheme (and edition) is named in your style sheet.
- [ ] Spot-check a sample of items against the official table: zero deviations.
- [ ] Established names and personal preferences are listed as exceptions.
- [ ] If reversibility was required, a back-conversion reproduces the source.
- [ ] Text is NFC-normalised; diacritics render in the target system.

## Checked
2026-11-01. Confirmed: ALA-LC table index (languages/scripts covered, approval by LC and ALA); BGN/PCGN systems jointly agreed by US BGN and PCGN, Russian table on gov.uk (UK MoD); NFC definition in Unicode UAX #15. Removed (not stated on pages read): ISO 7098, the Korean RR date, Japan's Kunrei/Hepburn status, passport and ICAO rules, Hunterian, ELOT/ISO 843, code point numbers, ICU transform IDs, per-scheme assignments to languages.
Method: documentation only; no commands were run.
