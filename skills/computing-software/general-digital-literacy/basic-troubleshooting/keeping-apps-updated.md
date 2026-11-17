---
id: computing-software.general-digital-literacy.basic-troubleshooting.keeping-apps-updated
name: keeping-apps-updated
category: computing-software
field: general-digital-literacy
product: basic-troubleshooting
tags: [basic-troubleshooting, software-updates, app-updates, microsoft-store, app-store, winget, auto-update]
level: intro
status: docs-checked
description: "Keep apps updated on Windows, Mac, iPhone and Android with store auto-updates, winget and in-app updaters, and spot apps that no longer get security fixes."
sources:
  - https://learn.microsoft.com/en-us/windows/package-manager/winget/upgrade
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Keep apps updated

**Goal:** every app gets security fixes without you having to remember.

## Windows
- The Microsoft Store has its own update and auto-update settings; open the Store's Library or Settings and look for updates.
- Many desktop apps (browsers, video-call apps, Office) update themselves; if one does not, use its own Help or About menu to check for updates.
- **winget** updates many apps at once from a terminal (Windows Package Manager reference):
  - `winget upgrade` lists installed packages that have updates.
  - `winget upgrade --all` upgrades all installed packages to the latest available version.
  - Add `--include-unknown` (short form `-u`) to include packages whose current version cannot be determined.

## Mac, iPhone, iPad, Android
Each store has an updates screen and an automatic-updates switch (Mac App Store, iPhone App Store settings, Google Play).
Menu paths change between OS versions: search the Settings app for "updates" or "automatic updates" and turn it on.
Apps not from a store: use the app's own "Check for Updates".

## Abandoned apps
- An app that no longer appears in its store, or whose developer stopped releasing updates, no longer gets security fixes: replace it.
- Uninstall old browser plug-ins and utilities you no longer use; they are common attack routes.

## Gotchas
- Restart the app (or computer) after updating; many updates apply only on relaunch.
- Website pop-ups saying "your browser is out of date, click here" are scams; update only from the app or its store.

## Verify
- [ ] `winget upgrade` and the store update lists show nothing important pending.

## Checked
2026-10-28. Confirmed (Microsoft Learn, winget upgrade): `winget upgrade`, `winget upgrade --all`, `--include-unknown` (also
`-u`/`--unknown`). Removed (unconfirmed; Microsoft Support, Apple Mac help and Android pages cited were root or stub pages):
Store menu paths, Office update path, Windows Update "other Microsoft products", Homebrew commands, iPhone/Android menu
paths, "two years" abandonment rule.
Method: documentation only; no commands were run.
