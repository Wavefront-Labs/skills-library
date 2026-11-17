---
id: computing-software.general-digital-literacy.web-browsers.browser-security-and-phishing-signals
name: browser-security-and-phishing-signals
category: computing-software
field: general-digital-literacy
product: web-browsers
tags: [web-browsers, phishing, https, padlock, certificate-warning, certificate-error, fake-browser-alert, malicious-download, safe-browsing, deceptive-site-warning, lookalike-domain, browser-notification-scam, lookalike-domains]
level: intro
status: draft
description: "Read a browser's own security signals correctly: what the padlock actually promises, certificate warnings, fake tech-support pop-ups, and malicious downloads."
sources: []
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Browser security and phishing signals — what the browser is actually telling you

**Goal:** correctly interpret the security signals a browser already shows on every
page — the padlock, certificate warnings, download warnings, and fake pop-ups
impersonating the browser itself — instead of either ignoring them or over-trusting
them.

## 1. What the padlock/HTTPS actually means (and doesn't)
- The padlock icon and `https://` mean the connection between you and the site is
  **encrypted** — nobody on the network path can read or tamper with the traffic in
  transit.
- It does **not** mean the site is legitimate, honest, or safe to enter card details
  into. Scam sites get HTTPS certificates just as easily as real ones — free, automated
  certificate issuance (Let's Encrypt and similar) made this trivial years ago. Judge
  trustworthiness by the domain and the site's reputation (see
  searching-and-evaluating-sources), not by the padlock alone.
- Click the padlock to see the actual certificate/connection details if you want to
  check who the certificate was issued to — rarely necessary for everyday browsing, but
  useful when something feels off.

## 2. Certificate warnings — when to actually stop
A full-page warning ("Your connection is not private," "This site can't provide a
secure connection") means the browser could not verify the site's identity/encryption
properly.
- **For a site you don't know or weren't specifically trying to reach**: stop, don't
  click through "Advanced › Proceed anyway." This is the state a fake/intercepted
  connection shows.
- **For a site you manage yourself or a work/school internal tool** where you
  understand *why* it's showing (an expired cert on an internal server you know about,
  a self-signed cert on a home device like a router's admin page): proceeding is
  reasonable once you understand the specific cause — the warning exists to stop
  blind trust, not to be ignored by habit, but it's not an absolute never either.
- A certificate warning that appears on a site that **worked fine yesterday** and that
  you didn't change anything about is worth treating with more suspicion than one on a
  device you just set up, since the former suggests something changed on the network/
  site side.

## 3. Fake browser alerts and tech-support scams
- A full-screen pop-up claiming "Your computer is infected," often with a countdown
  timer, fake scanning animation, and a **phone number to call**, is not from Microsoft,
  Apple, or your antivirus — real security software never asks you to call a phone
  number. This is the same scam covered operationally in
  everyday-troubleshooting-method, section 5; the browser-specific detail is below.
- These often use the browser's own **fullscreen mode** or a loop that re-triggers a
  "leave page?" dialog to make the tab feel impossible to close normally.
  Close it via Task Manager (`Ctrl+Shift+Esc` › end the browser task) or Force Quit
  (macOS `Cmd+Option+Esc`) rather than clicking anything inside the alert itself,
  including an "X" that might be part of the fake page's image.
- A real browser or OS security warning never asks you to call a number or buy a gift
  card — any alert that does either is fake regardless of how official it looks.

## 4. Malicious downloads
- Browsers scan downloads against a known-bad-file list (Chrome/Edge's Safe Browsing,
  Firefox's equivalent) and warn before completing a flagged download — heed this;
  don't click "Keep anyway" / "Keep dangerous file" for something you didn't deliberately
  seek out.
- Check the **file extension** before opening anything downloaded: a document,
  invoice, or photo that ends `.exe`, `.scr`, `.js`, `.bat`, `.msi`, or `.vbs` is a
  program, not the file type it claims to be (see browser-essentials, section 3, for
  how to make extensions visible if they're hidden).
- A download that starts **automatically** without you clicking a download link/button
  is itself suspicious — legitimate sites don't auto-download executables; cancel it
  and leave the site.

## 5. Lookalike and spoofed domains
- Read the actual domain in the address bar carefully before trusting a page that looks
  like a bank, delivery company, or login page: extra words, hyphens, a different
  top-level domain (`.co` instead of `.com`), or a subdomain trick
  (`yourbank.com.security-check.net` — the real domain is `security-check.net`, not
  `yourbank.com`) are all common spoofing patterns.
- When in doubt about a link from an email or text, don't click it — type the
  organisation's known address directly into the address bar instead (same principle as
  searching-and-evaluating-sources, section 4).

## Verify
- [ ] You can explain what the padlock does and doesn't guarantee, without overstating it.
- [ ] A certificate warning on an unfamiliar site was not clicked through.
- [ ] You know to close a fake "infected" alert via Task Manager/Force Quit, not by
      clicking anything inside it.
- [ ] Downloaded files are checked by extension before opening, and flagged/unexpected
      downloads are not kept.
