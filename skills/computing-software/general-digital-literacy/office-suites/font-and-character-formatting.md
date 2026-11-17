---
id: computing-software.general-digital-literacy.office-suites.font-and-character-formatting
name: font-and-character-formatting
category: computing-software
field: general-digital-literacy
product: office-suites
tags: [office-suites, word-processing, text-formatting, font-formatting, bold, italic, underline, font-size, font-colour, highlight, superscript, change-case]
level: intro
status: docs-checked
description: "Apply and adjust font, size, bold/italic, colour, highlight, superscript and change case with ribbon and shortcuts in Word, Google Docs and LibreOffice."
sources:
  - https://support.microsoft.com/en-us/office/keyboard-shortcuts-in-word-95ef89dd-7142-4b50-afb2-f762f663ceb2
  - https://support.microsoft.com/en-us/word/format-text-as-superscript-or-subscript-in-word
  - https://support.microsoft.com/en-us/word/change-the-capitalization-or-case-of-text
  - https://support.google.com/docs/answer/179738
  - https://support.google.com/docs/answer/1663349
  - https://help.libreoffice.org/latest/en-US/text/swriter/04/01020000.html
  - https://help.libreoffice.org/latest/en-US/text/shared/04/01010000.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Font and character formatting

**Goal:** format text quickly and consistently.

## Shortcuts (Windows; on Mac use Cmd)
| Action | Word | Google Docs | LibreOffice |
|---|---|---|---|
| Bold / Italic / Underline | `Ctrl+B` / `I` / `U` | same | same |
| Bigger / smaller font | `Ctrl+Shift+>` / `<` | `Ctrl+Shift+.` / `,` | Format › Character |
| Superscript / subscript | `Ctrl+Shift++` / `Ctrl+Shift+-` | `Ctrl+.` / `Ctrl+,` | `Ctrl+Shift+P` / `Ctrl+Shift+B` |
| Change case | `Shift+F3` cycles, or Home › Change Case | Format › Text › Capitalization | Format › Text |
| Strikethrough | Font dialog | `Alt+Shift+5` | Format › Character |

## Method
1. Select the text first.
2. Use the ribbon/toolbar or shortcut. The Font dialog (`Ctrl+D` in Word) has the full set of
   effects; small caps is also `Ctrl+Shift+K`.
3. **Highlight** (marker colour) is for review notes, not design.

## Gotchas
- Formatting many headings by hand is slow and inconsistent; use **heading styles** instead
  (see `computing-software.general-digital-literacy.office-suites.heading-styles-and-navigation`).
- Typing ALL CAPS is harder to read; use change case or small caps.
- Fonts not installed on the reader's computer may be substituted; stick to common fonts or send a PDF.
- Pasted text brings foreign fonts with it: paste as plain text with `Ctrl+Shift+V` (Word "Paste text
  only", Google Docs "Paste without formatting") or `Ctrl+Alt+Shift+V` (LibreOffice unformatted text).
- Remove manual character formatting: `Ctrl+Space` (Word), `Ctrl+\` (Docs), `Ctrl+M` (LibreOffice).

## Verify
- [ ] Same-level text uses the same font and size throughout (check with the font box as you click).

## Checked
2026-10-27 against the Microsoft Word keyboard shortcuts and superscript/subscript pages (Microsoft 365),
the Google Docs shortcut and formatting help, and the LibreOffice shortcut help (master). Confirmed every
shortcut in the table and list. Corrected: Word subscript is Ctrl+Shift+Minus in current Word (not
Ctrl+=); LibreOffice Ctrl+]/[ was not in the shortcut list and was replaced by Format › Character; Word
plain-text paste is Ctrl+Shift+V. Method: documentation only; no commands were run.
