---
id: computing-software.general-digital-literacy.web-browsers.removing-browser-hijackers
name: removing-browser-hijackers
category: computing-software
field: general-digital-literacy
product: web-browsers
tags: [web-browsers, extensions, browser-hijacker, unwanted-extension, managed-by-your-organisation, search-redirect, adware, reset-browser]
level: intro
status: docs-checked
description: "Remove a browser hijacker that changed your homepage or search engine, injects ads or shows 'Managed by your organization' on a personal computer (Chrome steps)."
sources:
  - https://support.google.com/chrome/answer/2765944
  - https://support.google.com/chrome/answer/9281740
  - https://support.google.com/chrome/answer/3296214
  - https://support.microsoft.com/en-us/edge/microsoft-edge-notification-browser-defaults
  - https://support.microsoft.com/en-us/help/4027935
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Removing a malicious extension or hijacker

**Goal:** get the browser back to your own settings and keep it that way. Consumer-level cleanup only; for a work or school computer, ask the administrator.

## Symptoms (Chrome's list)
Pop-up ads and new tabs that will not go away; homepage or search engine keeps changing; unwanted extensions or toolbars keep coming back; redirects to unfamiliar pages or ads; alerts about a virus or infected device.

## Fix, in order
1. **Programs first.** Windows: Start > Settings > Apps > Installed apps > select the app > Uninstall. Mac: Finder > Applications > right-click the program > Move to Trash > empty the Trash. Remove only programs you do not recognise.
2. **Extensions.** Chrome: More > Extensions > Manage extensions; remove ones you do not recognise (Remove, then confirm). Edge: Extensions > Manage extensions, toggle off, or Remove from Microsoft Edge.
3. **"Managed by your organization" on a personal device.** Chrome: open `chrome://management` and `chrome://policy`; check whether you are signed in with a work or school account (profile icon; a custom domain address is a managed account); review policies you do not recognise. Chrome's help then points to steps 1, 2 and 4 and a restart.
4. **Reset settings.** Chrome: More > Settings > Reset settings > Restore settings to their original defaults > Reset settings (warning: this clears cookies and site data and disables extensions; see resetting-browser-settings). Afterwards turn on only extensions you trust.
5. **Intrusive ads.** Chrome: More > Settings > Privacy and security > Site settings > Additional content settings > Intrusive ads, and choose a default.
6. Restart Chrome and the computer.

## Chrome and Edge guard some settings automatically
Chrome checks at every launch whether programs changed your settings and restores safe defaults. Edge restores the default search engine and new tab page if third-party software changes them, and shows a notification.

## Prevent
Chrome's tips: beware sites offering contest prizes or free copyrighted content; beware password-protected zip files; be sceptical of warnings about viruses; avoid downloading from sites without HTTPS; pay attention to Safe Browsing download warnings; get updates from the program's official site, not from a pop-up.

## Verify
- [ ] After a restart, homepage and search engine stay as you set them; `chrome://policy` shows no policies you did not expect.

## Checked
Date: 2026-10-27. Documentation: Chrome Help "Remove unwanted ads, pop-ups & malware", "Check if your Chrome browser is managed", "Reset Chrome settings to default"; Microsoft Support "Microsoft Edge notification: browser defaults" and "Add, turn off, or remove extensions in Microsoft Edge", read in October 2026. Confirmed: symptoms, Windows and Mac uninstall paths, extension removal, management and policy pages, reset path, intrusive-ads path, automatic defaults, prevention list. Removed as unconfirmed: the Firefox and Safari steps, shortcut-target inspection, named scanners, and the claim that a scanner removes policy entries.
Method: documentation only; no commands were run.
