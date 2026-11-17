---
id: computing-software.general-digital-literacy.web-browsers.linking-to-highlighted-text
name: linking-to-highlighted-text
category: computing-software
field: general-digital-literacy
product: web-browsers
tags: [web-browsers, browser-page-tools, link-to-text-fragment, copy-link-to-highlight, text-fragments]
level: intro
status: docs-checked
description: "Share a link that scrolls to and highlights a passage on a web page with Chrome's Copy link to highlight, and how the text fragment in the address works and fails."
sources:
  - https://support.google.com/chrome/answer/10256233
  - https://developer.mozilla.org/en-US/docs/Web/URI/Reference/Fragment/Text_fragments
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Share a link to highlighted text

## How (Chrome, computer)
1. Open the page and highlight the text: click and hold, then drag.
2. Right-click the highlighted text and choose **Copy link to highlight**. If the option is missing, the feature may not work for that content.
3. Paste the link in an email or message.
4. To remove the highlight in the linked page, right-click the highlighted text and choose **Remove highlight**.

## What the link looks like
A **text fragment** is added after `#:~:text=`. MDN's syntax: `#:~:text=[prefix-,]textStart[,textEnd][,-suffix]`. Examples from MDN: `#:~:text=use` highlights the first instance of "use"; `#:~:text=human,URL` highlights a string starting with "human" and ending with "URL"; a `prefix-,` or `,-suffix` selects a later instance by the text before or after it.

## When it fails
Per MDN, if the fragment matches no text in the page, or the browser does not support text fragments, the whole fragment is ignored and the link opens at the top of the page.

## Verify
- [ ] Opening the copied link in a new window scrolls to and highlights the selected passage.

## Checked
Date: 2026-10-27. Documentation: Chrome Help "Share or link to quotes & text in Chrome" and MDN "Text fragments", read in October 2026. Confirmed: the Chrome steps, the Remove highlight option, the fragment syntax and examples, and the no-match or unsupported behaviour. Removed as unconfirmed: Edge, Safari and Firefox menu names and version numbers, the Android Chrome share route, and the reasons given for links failing on dynamic, PDF or paywalled pages.
Method: documentation only; no commands were run.
