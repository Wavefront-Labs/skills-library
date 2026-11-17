---
id: computing-software.general-digital-literacy.web-browsers.extension-updates-and-ownership-changes
name: extension-updates-and-ownership-changes
category: computing-software
field: general-digital-literacy
product: web-browsers
tags: [web-browsers, browser-extensions, extension-updates, unsupported-extensions, malicious-extensions]
level: intro
status: docs-checked
description: "Handle Chrome extensions that are disabled as unsupported or turn suspicious: find an alternative, remove, reset settings, and report abuse in Edge Add-ons."
sources:
  - https://support.google.com/chrome/answer/2664769
  - https://support.google.com/chrome/answer/2765944
  - https://support.microsoft.com/en-us/help/4027935
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Extension updates and ownership changes

## Unsupported extensions (Chrome)
Chrome and the Chrome Web Store require extensions to be up to date with new requirements, so Chrome may disable extensions that do not meet them. If one is disabled:
1. More > Extensions > Manage Extensions > find it > Details > More > **Find Alternatives**, and add one from the Web Store; or
2. **Remove** it; or
3. temporarily turn it back on with its toggle. Chrome says this works only for a limited period, so find an alternative first. On a managed browser the administrator can re-enable with policy.

## Signs an extension has turned bad
Chrome's unwanted-software symptoms: a changing homepage or search engine, extensions or toolbars that come back, redirects to unfamiliar pages, pop-up ads.
## What to do
1. Remove the extension (Chrome: right-click its icon > Remove from Chrome; Edge: right-click > Remove from Microsoft Edge > Remove).2. Run Chrome's Safety Check (Settings > Privacy and security) and reset settings if the search engine or homepage changed (see resetting-browser-settings).
3. Remove unwanted programs and scan the computer (see removing-browser-hijackers).
4. Report abuse: on the Edge Add-ons site select the extension > Report abuse.
5. Change passwords for sites you used while it was installed if you think it could read your data.

## Prevention
Keep few extensions; install only ones you trust (Chrome: "only approve extensions that you trust").

## Verify
- [ ] Every remaining extension has a purpose you know, and the homepage and search engine are unchanged.

## Checked
Date: 2026-10-27. Documentation: Chrome Help "Install and manage extensions" and "Remove unwanted ads, pop-ups & malware"; Microsoft Support "Add, turn off, or remove extensions in Microsoft Edge", read in October 2026. Confirmed: the unsupported-extension procedure and temporary re-enable limit, symptom list, removal paths and Edge report-abuse. Removed as unconfirmed: automatic-update timing, Force Update via developer mode, the Cyberhaven incident and sold-extension narrative, Firefox steps and store-badge claims.
Method: documentation only; no commands were run.
