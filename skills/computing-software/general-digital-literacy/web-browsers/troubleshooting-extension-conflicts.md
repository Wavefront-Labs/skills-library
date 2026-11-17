---
id: computing-software.general-digital-literacy.web-browsers.troubleshooting-extension-conflicts
name: troubleshooting-extension-conflicts
category: computing-software
field: general-digital-literacy
product: web-browsers
tags: [web-browsers, browser-extensions, extension-conflicts, half-split-testing, broken-websites]
level: intro
status: docs-checked
description: "Find which Chrome extension is breaking a website or slowing the browser using Incognito, turning extensions off, and testing one at a time (or by halves)."
sources:
  - https://support.google.com/chrome/answer/6098869
  - https://support.google.com/chrome/answer/6138475
  - https://support.google.com/chrome/answer/2664769
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Troubleshoot extension conflicts

Symptoms: a site's buttons do not work, a video will not play, pages look broken, or the browser is slow.

## Step 1: confirm it is an extension (Chrome's procedure)
Open the page in an Incognito window. If it works there, go back to a normal window; Chrome's help says to turn off all extensions (More > Extensions > Manage extensions), reload, and if that fixes it turn extensions back on one at a time, reloading after each, to find the cause. If it is still broken in Incognito with extensions off, delete browsing data, then check the connection and the site (see page-will-not-load).

## Step 2: find the culprit faster (optional method)
Instead of one at a time, switch off half of the enabled extensions and reload. If fixed, the culprit is in the half you switched off; otherwise in the other half. Repeat on the guilty half until one remains. Sixteen extensions need at most four rounds.

## Fix
- Remove the extension that breaks the site (Remove, then confirm), or look for an alternative; Chrome's Details > More > Find Alternatives lists them.
- If an extension looks corrupted, Repair it (Manage extensions > Repair).
- Keep extensions limited to the sites they need (see reviewing-extension-permissions).

## Verify
- [ ] The site works with the remaining extensions on.

## Checked
Date: 2026-10-27. Documentation: Chrome Help "Fix connection and loading errors in Chrome", "Fix videos & games that won't play" and "Install and manage extensions", read in October 2026. Confirmed: the Incognito test, disable-all then re-enable one at a time, delete-browsing-data step, Repair and Find Alternatives. The halving procedure is a general testing method, not a documented Chrome feature. Removed as unconfirmed: Firefox Troubleshoot Mode, Guest profile test, the list of usual suspect extension types, and per-extension allowlist advice.
Method: documentation only; no commands were run.
