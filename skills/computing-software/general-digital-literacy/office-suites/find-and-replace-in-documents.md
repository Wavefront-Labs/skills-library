---
id: computing-software.general-digital-literacy.office-suites.find-and-replace-in-documents
name: find-and-replace-in-documents
category: computing-software
field: general-digital-literacy
product: office-suites
tags: [office-suites, word-processing, find-and-replace, find, replace-all, wildcards, regular-expressions, match-case, whole-words, special-characters]
level: intro
status: docs-checked
description: "Use Find and Replace safely in Word, Google Docs and LibreOffice: match case, whole words, special characters like paragraph marks, wildcards and regex."
sources:
  - https://support.microsoft.com/en-us/word/training/find-and-replace-text-in-word
  - https://support.microsoft.com/en-us/office/keyboard-shortcuts-in-word-95ef89dd-7142-4b50-afb2-f762f663ceb2
  - https://support.google.com/docs/answer/62754
  - https://support.google.com/docs/answer/179738
  - https://help.libreoffice.org/latest/en-US/text/shared/01/02100000.html
  - https://help.libreoffice.org/latest/en-US/text/shared/01/02100001.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Find and replace

**Goal:** change every occurrence correctly, and only the right ones.

## Open it
- Find: `Ctrl+F` in Word, Google Docs and LibreOffice.
- Replace: `Ctrl+H` in Word, Google Docs and LibreOffice (Google Docs on Mac: `Cmd+Shift+H`).

## Do it safely
1. Narrow the search: **Match case** (Word: More › Match case; Docs: Match case) and, where offered,
   whole words (LibreOffice: *Whole words only*). Without whole words, replacing "cat" also changes
   "category".
2. Click **Find Next** and **Replace** a few times to check before **Replace All**; Microsoft
   recommends Replace over Replace All so you can review each change.

## Special characters (Word)
In the Advanced Find & Replace dialog click More › **Special** to insert paragraph marks, tabs, page
breaks and other special characters into *Find what* or *Replace with*. Footnote and endnote
reference marks can be found as `^f` and `^e`.

## Patterns
- **Word:** tick *Use wildcards*: `s?t` finds "sat" and "set", `s*d` any string between,
  `10{1,3}` finds "10", "100" and "1000". Group with parentheses and reorder in *Replace with*:
  find `(Newman) (Belinda)`, replace `\2 \1`. Put `\` before a wildcard character to find it literally.
- **LibreOffice:** tick *Regular expressions* (ICU syntax): `\b` marks a word boundary; in *Replace*,
  `$1`, `$2` insert captured groups and `&` or `$0` the whole match.
- **Google Docs:** tick *Match using regular expressions* (RE2 syntax) for **Find** only. In Docs,
  anything typed in *Replace with* is inserted literally (capture-group replacements work only in
  Sheets), and `^`/`$` anchors are Sheets-only.

## Gotchas
- Formatting can be found and replaced too (Word: More › Format), handy for swapping a font or
  highlight.
- Text in headers, footers and text boxes: check them once by eye after a big replace.

## Verify
- [ ] Spot-check several replacements against what you expected.

## Checked
2026-10-27 against Microsoft Support (Find and replace text in Word; Word keyboard shortcuts), Google Docs
Editors Help (find and replace; shortcuts) and the LibreOffice help (master). Confirmed: Ctrl+F/Ctrl+H
in all three, Match case and Whole words only, Word Special menu, ^f/^e codes and wildcard examples,
LibreOffice $1/& replacement syntax. Corrected: Google Docs regex replacement with $1 and trailing-space
anchors do not work in Docs. Removed unconfirmed Word ^p/^t codes and undo claim.
Method: documentation only; no commands were run.
