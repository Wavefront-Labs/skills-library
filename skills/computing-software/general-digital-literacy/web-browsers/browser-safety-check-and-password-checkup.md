---
id: computing-software.general-digital-literacy.web-browsers.browser-safety-check-and-password-checkup
name: browser-safety-check-and-password-checkup
category: computing-software
field: general-digital-literacy
product: web-browsers
tags: [web-browsers, browser-privacy, safety-check, password-checkup, compromised-passwords]
level: intro
status: docs-checked
description: "Run Chrome Safety Check and Password Manager Checkup to find compromised, reused or weak passwords, harmful extensions and risky settings, then fix them."
sources:
  - https://support.google.com/chrome/answer/10468685
  - https://support.google.com/chrome/answer/95606
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Safety check and password checkup

## Chrome Safety Check
Chrome runs Safety Check automatically; to review it on a computer: More > Settings > Privacy and security > under "Safety Check" select **Go to Safety Check**, then select any item with an issue and follow the instructions.
It looks for:
- compromised, reused or weak passwords in Google Password Manager (warns if a stored username or password was in a data breach);
- Safe Browsing status and available Chrome updates;
- potentially unwanted or abusive notifications and unused site permissions (Chrome removes permissions from sites you have not used recently);
- potentially harmful extensions.

## Password Checkup
In Chrome's password manager, select **Checkup** (on the left) to see passwords exposed in a data breach and weak, easy-to-guess ones. To get alerts, More > Settings > Privacy and security > Security > Advanced > turn on "Warn you if a password was compromised in a data breach". Chrome recommends changing compromised passwords as soon as you can, on the site where the password is used, and checking other sites where the same password is saved.

## Acting on results
Change compromised passwords first (email, banking), on the real site, to unique ones. If your Google Account password may be compromised, change it immediately (Google's "Secure a hacked or compromised Google Account" page). Then fix reused and weak ones.

## Verify
- [ ] Re-run Safety Check: no compromised passwords flagged, no harmful extensions, Chrome up to date.

## Checked
Date: 2026-10-27. Documentation: Chrome Help "Manage Chrome safety and security" and "Manage passwords in Chrome", read in October 2026. Confirmed: Safety Check path and list of checks, Checkup, the breach-warning setting and path. Removed as unconfirmed: Privacy Guide, the passwords.google.com Password Checkup claim, Edge Password Monitor and SmartScreen paths, Firefox Monitor and Safari Security Recommendations steps.
Method: documentation only; no commands were run.
