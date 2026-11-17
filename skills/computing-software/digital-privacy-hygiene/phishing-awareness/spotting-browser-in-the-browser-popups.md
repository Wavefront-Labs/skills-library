---
id: computing-software.digital-privacy-hygiene.phishing-awareness.spotting-browser-in-the-browser-popups
name: spotting-browser-in-the-browser-popups
category: computing-software
field: digital-privacy-hygiene
product: phishing-awareness
tags: [digital-privacy-hygiene, phishing-awareness, browser-in-the-browser, bitb, oauth-phishing, sso-phishing, credential-theft, passkeys]
level: practitioner
status: draft
description: "Detect browser-in-the-browser phishing: fake 'Sign in with Google/Microsoft' popups drawn inside the page with a forged address bar, and the controls that defeat them."
sources:
  - "https://mrd0x.com/browser-in-the-browser-phishing-attack/"
  - "https://fidoalliance.org/passkeys/"
  - "https://www.cisa.gov/secure-our-world"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Spotting browser-in-the-browser popups

**Goal:** a fake login "window" can show a perfect `accounts.google.com` address bar because it is just HTML inside
the attacker's page. Learn the checks that a drawn window fails.

## The technique
Published in 2022 (mr.d0x), widely used against Steam, Microsoft 365 and crypto users. The page draws a window
with title bar, padlock and URL entirely in HTML/CSS/JS, mimicking an OAuth single-sign-on popup.

## Physical tests
- **Drag it**: drag the popup by its title bar toward the edge of the browser. A real window can leave the browser
  area; a fake one is clipped by the page.
- **Taskbar/dock**: a real popup appears as a separate window (Alt+Tab, Mission Control); the fake does not.
- **Maximise/minimise** buttons on the fake often do nothing or behave oddly.
- **Click into the address bar** and try to select or edit the URL; on fakes it is just an image or text.

## Tools that defeat it
- **Password manager autofill**: it fills by the real page origin, so it offers nothing on the attacker's domain.
  No autofill on a familiar login = stop.
- **Passkeys and security keys** are bound to the real origin; they will not work on the fake page.
- Sign in by typing the provider's address yourself in a new tab, then return to the site.

## If you entered credentials
Change the password from a clean session immediately, revoke sessions, check MFA methods and app passwords, and
review connected apps; see the phishing-page response checklist.

## Verify
- [ ] You habitually check autofill and can do the drag test before typing a password into any popup.
