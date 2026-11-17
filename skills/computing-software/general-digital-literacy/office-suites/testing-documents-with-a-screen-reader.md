---
id: computing-software.general-digital-literacy.office-suites.testing-documents-with-a-screen-reader
name: testing-documents-with-a-screen-reader
category: computing-software
field: general-digital-literacy
product: office-suites
tags: [office-suites, accessible-documents, screen-reader-testing, nvda, voiceover, narrator]
level: practitioner
status: docs-checked
description: "Check a document or slide deck with NVDA or Narrator: heading navigation, graphics, table headers, reading order and links."
sources:
  - https://download.nvaccess.org/releases/2026.2/documentation/userGuide.html
  - https://support.microsoft.com/en-us/windows/chapter-7-customizing-narrator-ce950246-c915-0d44-9be6-fb474387a285
  - https://support.apple.com/guide/voiceover/welcome/mac
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Test with a screen reader

The Accessibility Checker catches missing data; a quick screen-reader pass catches what it cannot (confusing alt text, wrong reading order, meaningless links).

## Tools
- **NVDA** (free, Windows). The installer can assign **Ctrl+Alt+N** to start it. The NVDA key is **Insert** by default (CapsLock can be chosen instead).
- **Narrator** (built into Windows): **Windows key+Ctrl+Enter** starts and stops it.
- **VoiceOver** (Mac): see Apple's VoiceOver User Guide for the current keys.

## 10-minute test (Word in NVDA browse mode)
1. **H**: jump heading to heading (Shift+letter goes back). Every section should be reachable and levels logical.
2. **NVDA+F7** opens the Elements List (in Word browse mode), which lists links, headings and more.
3. **G**: graphics. Each image should read meaningful alt text or be skipped as decorative.
4. **T**: next table; in a table **Ctrl+Alt+arrow keys** move between cells, and column headers should be announced.
5. **K**: links. Each should make sense alone.
6. **NVDA+Down Arrow** (Say All, desktop layout): listen to a page; the order should match the visual order.
7. PowerPoint: start the slide show and arrow through; each slide's title should be read first.

## Fix-and-retest loop
Fix in the source document (styles, alt text, reading order, table header row), re-export if needed, retest.

## Verify
- [ ] Heading list is complete, images are described, tables announce headers, reading order matches.

## Checked

2026-10-27. NVDA 2026.2 user guide (Ctrl+Alt+N installer option, Insert default NVDA key, single-letter navigation, table Ctrl+Alt+arrows, NVDA+F7 Elements List in Word, Say All NVDA+Down Arrow) and Microsoft Narrator guide (Windows+Ctrl+Enter), read 2026-10-27. Removed: VoiceOver key combinations and Rotor commands (not confirmed), the untagged-PDF claim, and the Insert+F7 'landmarks in Word' wording.

Method: documentation only; no commands were run.
