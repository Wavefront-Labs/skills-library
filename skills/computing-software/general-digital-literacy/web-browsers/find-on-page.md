---
id: computing-software.general-digital-literacy.web-browsers.find-on-page
name: find-on-page
category: computing-software
field: general-digital-literacy
product: web-browsers
tags: [web-browsers, tabs, browser, find-on-page, ctrl-f, find-in-page]
level: intro
status: docs-checked
description: "Search for words on a web page with Ctrl+F or Cmd+F in Chrome, Edge and Safari, step through matches, and find text in scanned PDFs opened in Chrome."
sources:
  - https://support.google.com/chrome/answer/157179
  - https://support.google.com/chrome/answer/95759
  - https://support.microsoft.com/en-us/microsoft-edge/keyboard-shortcuts-in-microsoft-edge-50d3edab-30d9-c7e4-21ce-37fe2713cfad
  - https://support.apple.com/guide/safari/keyboard-shortcuts-and-gestures-cpsh003/mac
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Find on page

## Desktop shortcuts
| Action | Chrome | Edge | Safari (Mac) |
|---|---|---|---|
| Open find | Ctrl+F or F3 (Mac Cmd+F) | Ctrl+F or F3 (Mac Cmd+F) | Cmd+F |
| Next match | Ctrl+G (Mac Cmd+G) | Ctrl+G (Mac Cmd+G) | not on Apple's shortcuts page; check the Edit menu |
| Previous match | Ctrl+Shift+G (Mac Cmd+Shift+G) | Ctrl+Shift+G (Mac Cmd+Shift+G) | not on Apple's shortcuts page; check the Edit menu |

- Chrome on Mac: with the find bar open, Cmd+E searches for the text you have selected.
- Chrome: Ctrl+K or Ctrl+E searches from anywhere on the page (it puts a search in the address bar, not on the page).

## PDFs
When you open a scanned PDF in Chrome's PDF viewer, Chrome converts it with on-device OCR so you can search, highlight and copy its text; a multi-page scan can take a while and shows "Extracting text from PDF...". Other viewers may not do this, so text in a scan may be unfindable there.

## Gotchas
- Find only searches what the page has loaded. Pages that load more as you scroll (feeds, some shops) may need scrolling first, or use the site's own search.
- Text inside images cannot be found unless OCR has been applied.

## Verify
- [ ] Typing a word that appears on the page highlights it, and the next-match shortcut moves to the following one.

## Checked
2026-10-27. Chrome Help (keyboard shortcuts; Download a file, which describes PDF OCR), Microsoft's Edge shortcuts page and Apple's Safari shortcuts page were read. Confirmed the open, next and previous shortcuts and Chrome's OCR for scanned PDFs. Firefox and phone-browser find menus are not covered because those pages could not be confirmed. Method: documentation only; no commands were run.
