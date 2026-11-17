---
id: computing-software.general-digital-literacy.web-browsers.resetting-browser-settings
name: resetting-browser-settings
category: computing-software
field: general-digital-literacy
product: web-browsers
tags: [web-browsers, browser-troubleshooting, reset-browser, restore-defaults, new-profile]
level: intro
status: docs-checked
description: "Reset Chrome settings to default, know what changes and what is kept, how Chrome and Edge restore changed defaults on their own, and test with a new profile."
sources:
  - https://support.google.com/chrome/answer/3296214
  - https://support.google.com/chrome/answer/2765944
  - https://support.google.com/chrome/answer/2364824
  - https://support.microsoft.com/en-us/edge/microsoft-edge-notification-browser-defaults
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Resetting browser settings

**Goal:** fix persistent weirdness (redirects, changed search engine, odd settings) without reinstalling.

**Warning:** a reset changes settings on every device where you are signed in to Chrome, clears cookies and site data (you will be signed out of sites) and turns off extensions. Bookmarks and saved passwords are not deleted.

## Chrome: how
On a computer: More > Settings > Reset settings > Restore settings to their original defaults > Reset settings (`chrome://settings/reset`). On some Windows versions Chrome's help words the section "Reset and cleanup". Chrome says this is not a full reset: for example fonts and accessibility settings are not removed.

## What changes in Chrome
Default search engine, homepage and startup tabs, new tab page, pinned tabs, content settings (such as pop-up and microphone permissions), cookies and site data, and extensions and themes (turn extensions you trust back on at More > Extensions > Manage extensions).

## Automatic resets
Chrome checks on every launch whether programs changed your settings, and restores the default search engine, homepage, startup pages, pinned tabs and extensions to safe values if so. Microsoft Edge likewise restores your default search engine and new tab page if third-party software changes them, and shows a notification.

## Test with a new profile
Chrome: profile icon > Add Chrome profile, choose a name, photo and colour. If the problem is gone there, the old profile is the cause. Removing a profile erases its bookmarks, history, passwords and settings from the computer.

## If the settings menu will not open
Chrome says to uninstall Chrome and reinstall it from google.com/chrome; if problems return, a program on the computer may be changing the settings (see removing-browser-hijackers).

## Verify
- [ ] The original problem does not return after a restart.

## Checked
Date: 2026-10-27. Documentation: Chrome Help "Reset Chrome settings to default", "Remove unwanted ads, pop-ups & malware", "Manage Chrome with multiple profiles"; Microsoft Support "Microsoft Edge notification: browser defaults", read in October 2026. Confirmed: the reset path, what changes, what is kept (bookmarks, passwords), the all-devices effect, automatic resets, profile removal warning. Removed as unconfirmed: the Edge reset menu path, the Firefox Refresh and Troubleshoot Mode steps, the Safari advice, and claims about history being kept.
Method: documentation only; no commands were run.
