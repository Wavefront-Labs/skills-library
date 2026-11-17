---
id: computing-software.digital-privacy-hygiene.password-hygiene.sites-that-block-paste
name: sites-that-block-paste
category: computing-software
field: digital-privacy-hygiene
product: password-hygiene
tags: [digital-privacy-hygiene, password-hygiene, paste-blocking, password-manager, autofill, nist-800-63b]
level: practitioner
status: draft
description: "Get long generated passwords into sites that block paste using autofill, auto-type and browser tricks, and push the site to fix it per NIST guidance."
sources:
  - "https://pages.nist.gov/800-63-4/sp800-63b.html"
  - "https://keepassxc.org/docs/KeePassXC_UserGuide#_auto_type"
  - "https://www.ncsc.gov.uk/blog-post/let-them-paste-passwords"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Sites that block paste

**Goal:** keep using a strong random password even when a form disables paste.

## Workarounds, in order
1. **Autofill** from the password manager extension usually sets the value directly and is not blocked by paste
   handlers.
2. **Auto-type** (KeePassXC Ctrl+Shift+V global auto-type, or Bitwarden's autotype on desktop where available)
   types keystrokes, which nothing can block.
3. **Mobile:** the OS autofill service bypasses paste blocks.
4. **Browser developer tools:** right-click the field > Inspect, then in the console set the value
   (`$0.value = '...'`) and dispatch an input event; clumsy, last resort.
5. **Firefox:** `about:config` > `dom.event.clipboardevents.enabled = false` stops sites from intercepting clipboard
   events (may break some web editors).

Never shorten or simplify the password to type it by hand.

## Ask them to fix it
NIST SP 800-63B-4 says verifiers SHALL allow password managers and autofill, and SHOULD permit paste. The UK NCSC
blog "Let them paste passwords" makes the same case. Send the site a short note citing both.

## Confirm-password fields
If only the confirmation field blocks paste, autofill both or use auto-type for the second field. Check you can log
in before closing the tab.
