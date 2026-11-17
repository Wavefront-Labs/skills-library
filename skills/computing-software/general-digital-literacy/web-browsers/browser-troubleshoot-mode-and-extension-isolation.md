---
id: computing-software.general-digital-literacy.web-browsers.browser-troubleshoot-mode-and-extension-isolation
name: browser-troubleshoot-mode-and-extension-isolation
category: computing-software
field: general-digital-literacy
product: web-browsers
tags: [troubleshoot-mode, safe-mode, disable-extensions, browser-profile, isolation]
level: practitioner
status: draft
description: "Isolate browser problems using Firefox Troubleshoot Mode, Chrome extensions off or guest profile, and a new profile, then find the faulty extension or setting."
sources: ["https://support.mozilla.org/", "https://support.google.com/chrome/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Troubleshoot mode and isolating extensions

**Goal:** decide quickly whether an extension, setting or profile is the cause.

## Test without customisations
- Firefox **Troubleshoot Mode** (Menu > Help > Troubleshoot Mode, formerly Safe Mode): restarts with extensions, themes, hardware acceleration and many settings turned off for the session, without changing your profile. Choose Restart, not Refresh, to keep data.
- Chrome/Edge: open the site in a **Guest** or new profile (extensions are not there), or an Incognito/InPrivate window with extensions not allowed; or launch with extensions disabled from the command line for testing.
- Safari: Settings > Extensions, switch off all, retest.

## Interpret
- Fixed in troubleshoot mode/new profile: an extension, theme, setting or profile corruption is responsible.
- Not fixed: the site, network, DNS, antivirus, or driver (see hardware acceleration skill).

## Find the culprit
1. Re-enable extensions in halves (bisect), retesting each time.
2. Check recent changes (extension updates, new installs).
3. Reset settings, or create a fresh profile and sync back only what you need (bookmarks, passwords) instead of all extensions at once.
4. Remove extensions you no longer need; report the bug to the developer.

## Verify
The problem reappears only when the identified extension is enabled and disappears when it is off.
