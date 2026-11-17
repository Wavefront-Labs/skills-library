---
id: computing-software.general-digital-literacy.web-browsers.blocked-and-dangerous-downloads
name: blocked-and-dangerous-downloads
category: computing-software
field: general-digital-literacy
product: web-browsers
tags: [web-browsers, downloads, blocked-download, dangerous-download, safe-browsing, insecure-download, unverified-download]
level: intro
status: docs-checked
description: "Understand Chrome's download warnings (dangerous, suspicious, unverified, insecure) and decide safely whether to keep or delete the file."
sources:
  - https://support.google.com/chrome/answer/6261569
  - https://support.google.com/chrome/answer/9890866
  - https://support.google.com/chrome/answer/2765944
  - https://support.apple.com/guide/safari/download-items-from-the-web-sfri40598/mac
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Blocked or dangerous download warnings

**Goal:** know what each warning means before overriding it.

## Chrome's warning types
| Type | Means | Usual action |
|---|---|---|
| Dangerous | Malware, or deceptive software that could change your device or settings | Do not keep it |
| Suspicious | An uncommon or unfamiliar file, or one that may hide malware, such as inside a .zip or .rar archive (a password may be added to avoid detection) | Verify the source first |
| Unverified | Downloaded while Safe Browsing was turned off | Turn Safe Browsing back on and check the file |
| Insecure | Delivered over a connection that is not HTTPS, even if the page was secure | Get it from an HTTPS source |

Chrome blocks dangerous downloads automatically; you can still choose to download after a warning, but Chrome says to take warnings seriously, because attackers may ask you to turn off or ignore warnings to avoid antivirus detection. A blocked-download warning leaves your history after one hour, or sooner with **Delete from history**.

## Decide
1. Did you deliberately download it from the official site (typed the address or used a bookmark)?
2. Is the file type expected? An "invoice" or "video player" that is an executable is a red flag.
3. If unsure, delete it and get it from the vendor's own website or an app store.
4. Password-protected archives: with Standard protection Chrome can check some .zip, .7z and .rar files locally if you enter the file's password and select **Check for malware**; with Enhanced protection you can send a suspicious file to Safe Browsing for a scan.

## Gotchas
- Beware of sites that push downloads for contests or free copyrighted content, encrypted archives that may bypass antivirus scans, and warnings about viruses you did not trigger. If a popup about a program update or download seems suspicious, go to the program's official website instead.
- Safari alerts you when you open a download that contains software; do not open software you did not expect or that is not from a trusted source.
- Edge and Firefox warning wording and override steps are not covered here (see Checked).

## Verify
- [ ] Chrome Settings > Privacy and security > Security shows Safe Browsing set to Standard or Enhanced protection.

## Checked
2026-10-27. Chrome Help (Google Chrome blocks some downloads; Choose your Safe Browsing protection level; Remove unwanted ads, pop-ups and malware) and Apple's Safari User Guide (Download items from the web) were read. Confirmed the warning types, the one-hour history behaviour, encrypted-file checking and the Safe Browsing menu path. Edge SmartScreen and Firefox messages are not covered because they could not be confirmed. Method: documentation only; no commands were run.
