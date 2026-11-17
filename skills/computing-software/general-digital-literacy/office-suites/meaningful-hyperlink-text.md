---
id: computing-software.general-digital-literacy.office-suites.meaningful-hyperlink-text
name: meaningful-hyperlink-text
category: computing-software
field: general-digital-literacy
product: office-suites
tags: [office-suites, accessible-documents, hyperlink-text, link-text, screentips, descriptive-links]
level: intro
status: docs-checked
description: "Write descriptive link text instead of 'click here' or raw URLs in documents, emails and slides, and edit display text and ScreenTips in Word and Docs."
sources:
  - https://www.w3.org/WAI/tips/writing/
  - https://support.microsoft.com/en-us/accessibility/word/keyboard-shortcuts-in-word
  - https://download.nvaccess.org/releases/2026.2/documentation/userGuide.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Meaningful hyperlink text

**Why:** screen-reader users often navigate by a list of links. Ten "click here" links are useless, and so are long URLs read out character by character. The W3C WAI writing tips advise making link text meaningful.

## Good vs bad
| Bad | Good |
|---|---|
| Click here to read the policy | Read the [travel expenses policy] |
| (a full pasted URL) | [Q3 report (PDF)] |
| More | [More about evening classes] |

Rules of thumb: link text makes sense out of context, describes the destination, mentions file type for downloads, is unique per destination, and is short.

## Edit link text
- Word (Windows): select the text and press **Ctrl+K** to insert a hyperlink, then fill in the text to display and address.
- Pasting a URL creates a link showing the raw address; replace the visible text with a description.

## Printed documents
If the document will be printed, show the address in brackets after the link text, or use a QR code.

## Check by listening
In Word with NVDA, **NVDA+F7** opens the Elements List (browse mode), which can list links; each link should tell you where it goes.

## Verify
- [ ] Reading only the links in order, each one still makes sense.

## Checked

2026-10-27. W3C WAI writing tips (meaningful link text), Microsoft Word keyboard shortcuts page (Ctrl+K insert hyperlink) and NVDA 2026.2 user guide (NVDA+F7 Elements List in Word browse mode), read 2026-10-27. Removed: Edit Link and ScreenTip steps, PowerPoint/Outlook/Google Docs shortcuts and the Accessibility Checker unclear-link claim (the rules page does not list it).

Method: documentation only; no commands were run.
