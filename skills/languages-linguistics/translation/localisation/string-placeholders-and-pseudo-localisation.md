---
id: languages-linguistics.translation.localisation.string-placeholders-and-pseudo-localisation
name: string-placeholders-and-pseudo-localisation
category: languages-linguistics
field: translation
product: localisation
tags: [localisation, localization, l10n, i18n, internationalization, software-localisation, game-localisation, website-localisation, ui-strings, string-length, text-expansion, placeholders, format-strings, icu-messageformat, plurals, cldr, gender, pseudo-localisation, pseudolocalization, locale-testing, linguistic-qa, lqa, rtl, bidi, xliff, po-files, gettext, json-resources, context-screenshots, string-freeze]
level: practitioner
status: draft
description: "Localise software and games without breaking them: protect placeholders and markup, handle plurals and gender with ICU rules, fit length limits, and catch problems early with pseudo-localisation."
sources: ["Unicode CLDR plural rules (cldr.unicode.org)", "ICU MessageFormat documentation (unicode-org.github.io/icu)", "W3C Internationalization guidance on bidi text"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# String placeholders and pseudo-localisation

**Goal:** translated strings that read naturally *and* don't crash the build, overflow
the UI, or break plurals — for apps, websites and games.

## 1. What the translator receives
Usually resource files (XLIFF, gettext PO, JSON, Android XML, iOS .strings/.xcstrings,
spreadsheet exports for games) with keys, source strings, sometimes comments, max-length
limits and screenshots. Ask for **context** (screenshots, string IDs grouped by screen,
a build to play) before starting — "Open" as a verb vs adjective, "Back" as button vs body
part, can't be guessed from a key alone.

## 2. Placeholders and markup — never break them
- Keep every variable exactly: `%s`, `%d`, `%1$s`, `{0}`, `{username}`, `{{count}}`, `$t(key)`.
  Reorder positional ones as grammar requires (`%1$s`/`%2$s`, `{0}`/`{1}`), never rename them.
- Keep tags balanced: `<b>…</b>`, `<color=#FF0>…</color>`, `\n`, escape sequences (`\"`, `&amp;`).
- Don't translate keys, URLs, colour codes or code identifiers.
- Concatenated fragments ("You have" + n + "new messages") are an i18n bug; report it instead
  of trying to make word order fit.

## 3. Plurals and gender
- Languages have different plural categories (CLDR: zero, one, two, few, many, other).
  English has 2 forms; Polish and Russian use more; Arabic uses all six; Japanese and Chinese
  usually only "other". ICU example:
  `{count, plural, one {# plik} few {# pliki} many {# plików} other {# pliku}}`
  — supply **every** category your language requires, even if the source shows only one/other.
- Gender: ICU `select` (`{gender, select, female {…} male {…} other {…}}`) where the system
  supports it; otherwise rephrase neutrally ("Player 2 joined" vs "he joined").

## 4. Length and layout
- Expect expansion: English → German/French/Russian often +20–35%, short strings far more
  (a 4-letter button can double); CJK usually shorter but needs larger font height.
- Respect max-length limits; abbreviate only with established abbreviations; ask for wider
  buttons rather than producing nonsense.
- RTL languages (Arabic, Hebrew): mixed-direction text (numbers, Latin brand names) needs
  correct bidi handling; check in context, not in the spreadsheet.

## 5. Pseudo-localisation (for the dev/loc team)
Before real translation, generate a pseudo-locale that:
- replaces letters with accented look-alikes (`Settings` → `[Šéţţîñĝš !!!]`) so hard-coded,
  non-externalised strings stand out (they stay plain English);
- pads length by ~30–40% to reveal truncation;
- wraps with brackets to show clipping at either end;
- optionally uses RTL-mirroring pseudo-locale for layout.
Run the app in it and log every bug before sending files to translators.

## 6. Linguistic QA (LQA)
Test the localised build: truncation, overlaps, untranslated strings, wrong plural/gender,
inconsistent terminology between UI and help, culturally inappropriate images/colours, date,
number and currency formats from the locale (not hand-written).

## Gotchas
- Translation memory reuse across platforms: "Tap" (mobile) vs "Click" (desktop).
- Fonts lacking glyphs show boxes (tofu) — test real target characters.
- Sorting, capitalisation and case conversion (Turkish dotted/dotless i) differ by locale.
- Games: lip-sync and voice-over timing, subtitles length per second, age-rating sensitivities
  per market.
- String freeze dates: late source changes cause untranslated text at release.

## Verify
- [ ] Automated QA shows zero placeholder/tag mismatches between source and target.
- [ ] Every plural string has all CLDR categories for the target language.
- [ ] Pseudo-locale run found no hard-coded strings left unfixed.
- [ ] LQA pass on a real build: no truncation, untranslated text or broken formats.
- [ ] Context questions answered and stored in comments/TM for the next release.

Related: `languages-linguistics.translation.technical-translation.terminology-consistency-and-controlled-language`,
`languages-linguistics.translation.transcreation.briefs-options-and-rationale`.
