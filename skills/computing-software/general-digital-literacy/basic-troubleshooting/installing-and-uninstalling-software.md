---
id: computing-software.general-digital-literacy.basic-troubleshooting.installing-and-uninstalling-software
name: installing-and-uninstalling-software
category: computing-software
field: general-digital-literacy
product: basic-troubleshooting
tags: [basic-troubleshooting, installing-software, uninstalling-software, admin-rights, user-account-control, uac, bundled-software, pup, potentially-unwanted-program, app-store, microsoft-store, driver-updates, portable-apps, software-sources]
level: intro
status: draft
description: "Install and remove desktop software safely: which sources to trust, what admin prompts actually mean, dodging bundled junk, and uninstalling cleanly."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Installing and uninstalling software — without inviting junk in

**Goal:** get software onto a computer from a source you can trust, understand the
permission prompt before clicking through it, and remove software completely rather than
leaving leftovers that cause the next odd bug.

## 1. Where to get software from (in order of trust)
1. **The OS's own store** (Microsoft Store, Mac App Store) — sandboxed, auto-updating,
   vetted, but a smaller catalogue.
2. **The vendor's own official site** — type the address yourself or reach it from a
   search result you've verified (see searching-and-evaluating-sources), never from a
   pop-up ad or a "download" button on a random forum thread.
3. **Package managers for technical users** (`winget`, Homebrew) — reproducible and easy
   to audit, but out of scope for most everyday users.
Avoid "download portal" sites that wrap a real installer in their own ad-laden
installer — the giveaway is a page offering a "Download now" button that is actually an
ad, with the real link buried or tiny.

## 2. Reading the admin prompt instead of reflexively accepting it
- Windows **User Account Control (UAC)** — the dimmed-screen "Do you want to allow this
  app to make changes to your device?" — appears for anything that installs system-wide
  or changes system settings. It should appear **once**, right after you clicked install.
  A UAC prompt appearing **unprompted**, with no app you just launched, is a red flag —
  cancel and investigate rather than clicking Yes out of habit.
- macOS asks for your **password or Touch ID** for the same reason, and for new apps not
  from the App Store will show a Gatekeeper warning the first time they're opened
  (System Settings › Privacy & Security has the override if you deliberately trust it).
- Never grant admin/password access to a program you didn't just choose to install.

## 3. Dodging bundled junk during install
Installers for free utilities (PDF tools, driver updaters, video converters) are the
classic vehicle for bundled toolbars, browser-homepage-changers and "optional" extra
programs.
- Always choose **Custom/Advanced install**, never "Express/Quick", the first time you
  run an unfamiliar installer — Express frequently pre-ticks the extras.
- Read each checkbox; untick anything you didn't ask for (a toolbar, a second antivirus,
  a "driver booster", a changed default search engine/homepage).
- If an installer's buttons are confusing on purpose (a big green "Accept" that's
  actually for the bundled extra, a tiny real "Decline" link), that vendor has a bad
  reputation — note it and prefer an alternative tool next time.

## 4. Uninstalling cleanly
- Windows: Settings › Apps › Installed apps, or right-click the Start entry › Uninstall.
  Don't just delete the folder/shortcut — that leaves registry entries and files behind.
- macOS: drag the `.app` from Applications to Trash **plus** check `~/Library/Application
  Support`, `~/Library/Preferences` and `~/Library/Caches` for a folder matching the
  app's name if you want it fully gone (most people can skip this for a normal app).
- After uninstalling, restart the browser and check its extensions/homepage/default
  search engine weren't changed by the app you just removed.
- A program that **won't uninstall** or has no entry in the list: try the vendor's own
  uninstaller/removal tool (search "<app name> uninstall tool"), or Windows' built-in
  **Fix problems that block programs from being installed or removed** troubleshooter.

## 5. Drivers specifically
Graphics, printer and audio drivers are software too, and the same trust rule applies:
get them from Windows Update, the laptop/GPU maker's own support page, or the printer
maker's site — not a generic "driver updater" tool, many of which are themselves
bundled-junk vehicles that flag drivers as "outdated" to sell a paid fix.

## Verify
- [ ] You can name the source the last app you installed came from, and why you trust it.
- [ ] You used Custom/Advanced install and unticked anything not explicitly wanted.
- [ ] No admin/password prompt was accepted for something you didn't just choose to run.
- [ ] An app you removed is gone from the installed-apps list, and your browser's
      homepage/search engine/extensions are unchanged.
