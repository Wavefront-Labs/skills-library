---
id: computing-software.general-digital-literacy.office-suites.spelling-grammar-and-proofing-language
name: spelling-grammar-and-proofing-language
category: computing-software
field: general-digital-literacy
product: office-suites
tags: [office-suites, word-processing, spelling-and-grammar, proofing, spellcheck, proofing-language, editor, custom-dictionary, autocorrect]
level: intro
status: draft
description: "Run spelling and grammar checks, set the proofing language (UK vs US English), manage the custom dictionary and AutoCorrect in Word, Google Docs and LibreOffice."
sources:
  - https://support.microsoft.com/en-us/word
  - https://support.google.com/docs
  - https://help.libreoffice.org/latest/en-US/text/shared/main0000.html
  - https://icdl.org/programmes/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Spelling, grammar and proofing language

**Goal:** catch errors, in the right variety of the language.

## Run the check
- **Word:** `F7` or Review › Editor. Red underline = spelling, blue double = grammar/clarity.
- **Google Docs:** Tools › Spelling and grammar › Spelling and grammar check (`Ctrl+Alt+X`).
- **LibreOffice:** `F7` or Tools › Spelling. Toggle auto-check with `Shift+F7`.

## Set the language (the most common cause of "everything is wrong")
- **Word:** select all (`Ctrl+A`) › Review › Language › Set Proofing Language › English (United
  Kingdom) › optionally "Set As Default". Pasted text often carries another language tag.
- **Google Docs:** File › Language.
- **LibreOffice:** Tools › Language › For All Text › choose.
"Do not check spelling or grammar" ticked in Word's language box silently disables checking on
that text; untick it.

## Dictionary and AutoCorrect
- Right-click a flagged word › **Add to Dictionary** for names and jargon. Word's list: File ›
  Options › Proofing › Custom Dictionaries.
- AutoCorrect (Word File › Options › Proofing › AutoCorrect Options; LibreOffice Tools ›
  AutoCorrect Options) fixes typos as you type and expands shortcuts, e.g. `(c)` to ©. Remove
  entries that misfire.

## Gotchas
- Spellcheckers pass real words used wrongly (their/there, form/from, manager/manger). Read it
  aloud (Word Review › Read Aloud) or have someone else read.
- Don't accept grammar suggestions blindly; they can change meaning.

## Verify
- [ ] Status bar shows the intended language; F7 reports no unreviewed issues.
