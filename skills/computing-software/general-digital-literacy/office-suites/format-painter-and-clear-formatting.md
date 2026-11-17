---
id: computing-software.general-digital-literacy.office-suites.format-painter-and-clear-formatting
name: format-painter-and-clear-formatting
category: computing-software
field: general-digital-literacy
product: office-suites
tags: [office-suites, word-processing, format-painter, clear-formatting, paint-format, clone-formatting, paste-text-only, keep-text-only]
level: intro
status: docs-checked
description: "Copy formatting with Format Painter / Paint format and strip messy formatting with Clear Formatting or paste-as-plain-text in Word, Google Docs and LibreOffice."
sources:
  - https://support.microsoft.com/en-us/word/use-the-format-painter
  - https://support.microsoft.com/en-us/office/keyboard-shortcuts-in-word-95ef89dd-7142-4b50-afb2-f762f663ceb2
  - https://support.microsoft.com/en-us/word/control-the-formatting-when-you-paste-text
  - https://support.google.com/docs/answer/179738
  - https://help.libreoffice.org/latest/en-US/text/shared/02/paintbrush.html
  - https://help.libreoffice.org/latest/en-US/text/shared/04/01010000.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Format Painter and clearing formatting

**Goal:** make text match other text in two clicks, and remove junk formatting.

## Copy formatting
- **Word:** select the source text › Home › **Format Painter** › select the target. A single click
  paints once; **double-click** the button to paint many places, `Esc` to stop.
  Keyboard: `Ctrl+Alt+C` copy formatting, `Ctrl+Alt+V` paste formatting.
- **Google Docs:** `Ctrl+Alt+C` copy text formatting, `Ctrl+Alt+V` paste text formatting (Mac:
  `Cmd+Option+C` / `Cmd+Option+V`).
- **LibreOffice:** select the source › **Clone Formatting** (paintbrush; Format › Clone Formatting) ›
  click or drag across the target.

## Clear formatting
- Word: select › `Ctrl+Space` removes manual character formatting, `Ctrl+Q` removes paragraph formatting.
- Google Docs: `Ctrl+\` clears text formatting.
- LibreOffice: `Ctrl+M` (Format › Clear Direct Formatting).

## Paste without formatting
- Google Docs: `Ctrl+Shift+V` (paste without formatting).
- LibreOffice: `Ctrl+Alt+Shift+V` pastes unformatted text; `Ctrl+Shift+V` opens Paste Special.
- Word: `Ctrl+Shift+V` (paste text only), or the Paste Options **Keep Text Only**; to make it the
  default set File › Options › Advanced › *Pasting from other programs* to Keep Text Only.

## Gotchas
- Clearing formatting also removes bold/italic you wanted. Do it before the final formatting pass.
- If the same look repeats across a document, define or update a **style** instead of painting;
  then a single style change updates everything.

## Verify
- [ ] Pasted text uses the document's font, not the website's.

## Checked
2026-10-27 against Microsoft Support (Use the Format Painter; Word keyboard shortcuts; paste formatting
options), Google Docs keyboard shortcuts and the LibreOffice help (master). Confirmed every shortcut and
menu path listed. Corrected: Word copy/paste formatting is Ctrl+Alt+C / Ctrl+Alt+V in current Word (the
page no longer lists Ctrl+Shift+C/V). Removed unconfirmed toolbar-icon and double-click claims for Docs and
LibreOffice. Method: documentation only; no commands were run.
