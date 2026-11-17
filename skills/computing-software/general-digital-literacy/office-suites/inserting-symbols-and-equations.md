---
id: computing-software.general-digital-literacy.office-suites.inserting-symbols-and-equations
name: inserting-symbols-and-equations
category: computing-software
field: general-digital-literacy
product: office-suites
tags: [office-suites, text-formatting, insert-symbol, special-characters, equations, alt-codes, emoji-panel]
level: intro
status: docs-checked
description: "Type symbols, accented letters and equations in Word, Google Docs and any app: Symbol dialog, AutoCorrect codes, Windows emoji panel and Mac Character Viewer."
sources:
  - https://support.microsoft.com/en-au/word/insert-ascii-or-unicode-character-codes-in-word
  - https://support.microsoft.com/en-us/word/format-text-as-superscript-or-subscript-in-word
  - https://support.microsoft.com/en-us/word/autoformat-as-you-type
  - https://support.microsoft.com/en-us/office/keyboard-shortcuts-in-word-95ef89dd-7142-4b50-afb2-f762f663ceb2
  - https://support.microsoft.com/en-us/accessibility/office-accessibility/use-keyboard-to-work-with-equations
  - https://support.google.com/docs/answer/3371015
  - https://support.google.com/docs/answer/160749
  - https://support.microsoft.com/en-us/windows/hardware/input-devices/windows-keyboard-tips-and-tricks
  - https://support.apple.com/guide/mac-help/mchlp1560/mac
  - https://support.apple.com/guide/mac-help/enter-characters-with-accent-marks-on-mac-mh27474/mac
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Inserting symbols, special characters and equations

## In Word
- **Insert › Symbol › More Symbols**: pick font *(normal text)*, choose a subset (e.g. Superscripts and
  Subscripts), **Insert**.
- Type the Unicode hex code then **Alt+X**: `221A` Alt+X = √, `0024` Alt+X = $. If the code follows
  other text, select just the code first. Alt+X on a selected character shows its code.
- Alt codes: hold Alt and type the decimal code on the numeric keypad with Num Lock on, e.g.
  Alt+0169 = ©, Alt+0128 = €.
- AutoCorrect as you type: `(c)` = ©; `--` with no spaces = em dash (—); space-hyphen-space = en dash (–).
- Non-breaking space: **Ctrl+Shift+Space** (keeps "10 kg" together). Non-breaking hyphen:
  **Alt+Shift+-** in current Word.
- Equations: **Alt+=** inserts an equation; type it in linear format and press **Ctrl+=** to convert
  to professional (built-up) format.

## In Google Docs
**Insert › Symbols › Special characters**: pick a category, enter a Unicode value, or draw the
character. **Insert › Symbols › Equation** for maths; in an equation type `\` plus a symbol name and a
space (e.g. `\alpha`).

## Anywhere on the OS
- Windows: **Windows key + .** (period) opens the emoji panel with GIFs, kaomoji and **Symbols**
  (punctuation, accented letters, currency and more).
- Mac: **Fn/Globe + E** or Edit › Emoji & Symbols opens the Character Viewer. Press and hold a letter
  key (e.g. a) for the accent menu; dead keys also work, e.g. Option-N then a = ã.

## Gotchas
- Symbols from decorative fonts such as Wingdings change if the recipient's font differs or the text is
  pasted elsewhere; prefer the *(normal text)* Unicode character.
- Screen readers may announce some symbols oddly; spell out meaning when it matters.

## Verify
- [ ] The character survives saving as PDF and pasting into a plain text editor.

## Checked
2026-10-27 against Microsoft Support (Unicode/ASCII codes in Word, superscript/subscript symbols,
AutoFormat As You Type, Word shortcuts, equation keyboard guide), Google Docs Editors Help (special
characters, equations), Microsoft Windows keyboard tips and Apple Mac User Guide. Confirmed every
shortcut and menu path listed. Corrected: Word non-breaking hyphen is Alt+Shift+Minus in the current
shortcut list; Docs menus are under Insert › Symbols; Mac Character Viewer is Fn/Globe+E. Removed
unconfirmed Option-key symbol shortcuts and phone tips. Method: documentation only; no commands were run.
