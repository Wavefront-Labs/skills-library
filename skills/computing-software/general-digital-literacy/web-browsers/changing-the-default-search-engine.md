---
id: computing-software.general-digital-literacy.web-browsers.changing-the-default-search-engine
name: changing-the-default-search-engine
category: computing-software
field: general-digital-literacy
product: web-browsers
tags: [web-browsers, browser-settings, default-search-engine, search-engine-hijack, address-bar-search, site-search-shortcuts]
level: intro
status: docs-checked
description: "Change the address-bar search engine in Chrome and Safari, add Chrome site search shortcuts and recognise a search engine changed by unwanted software."
sources:
  - https://support.google.com/chrome/answer/95426
  - https://support.apple.com/guide/safari/customize-searching-ibrwe75c2a3c/mac
  - https://support.apple.com/en-us/102192
  - https://support.google.com/chrome/answer/2765944
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Changing the default search engine

**Goal:** typing in the address bar searches with the engine you chose.

## Where
- **Chrome:** More > **Settings** > **Search engine** > under "Search engine" select **Change** and pick one. In some countries Google is the default; in others Chrome asks you to choose. On a work or school profile an administrator may set it.
- **Safari (Mac):** delete the text in the Smart Search field, click the magnifying glass icon to its left, and choose a search engine from the list. Search engines apply their own policies to the data they collect.
- Safari > Settings > Search also has switches for search-engine suggestions, Safari Suggestions, Quick Website Search and Preload Top Hit.

## Site search shortcuts (Chrome)
Settings > Search engine > **Manage search engines and site search**. Next to "Site search" select **Add** and fill in the *Search engine* (a name), *Shortcut* (the text you type in the address bar) and *URL with %s in place of query*. To get the URL, run a search on that site, copy the results-page address and replace the search term with `%s`. You can edit, make default, deactivate or delete a shortcut from its More menu. Gemini cannot be edited, deleted or set as default.

## Search changed by itself?
- Chrome says unexpected changes to your search engine may mean malware; see Chrome's "Remove unwanted ads, pop-ups & malware" page and reset settings if needed. Chrome also checks at each launch whether unwanted programs changed your settings and may restore them.
- Apple says that if Safari keeps changing the search engine or reopening windows, a phishing site may have tricked you into installing unwanted software: update macOS, restart, and remove unknown apps and Safari extensions.

## Verify
- [ ] Type a word in the address bar: results come from your chosen engine.

## Checked
2026-10-27. Chrome Help (Set default search engine and site search shortcuts; Remove unwanted ads, pop-ups and malware) and Apple Support (Customise searching in Safari; Control which windows Safari reopens) were read. Confirmed the Chrome and Safari steps and hijack guidance above. Edge and Firefox settings and phone-app menus are not covered because they could not be confirmed. Method: documentation only; no commands were run.
