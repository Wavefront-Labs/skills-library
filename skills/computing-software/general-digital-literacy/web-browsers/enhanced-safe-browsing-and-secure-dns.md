---
id: computing-software.general-digital-literacy.web-browsers.enhanced-safe-browsing-and-secure-dns
name: enhanced-safe-browsing-and-secure-dns
category: computing-software
field: general-digital-literacy
product: web-browsers
tags: [web-browsers, browser-privacy, enhanced-safe-browsing, secure-dns, dns-over-https, enhanced-protection, https-only-mode]
level: intro
status: docs-checked
description: "Set Chrome's Safe Browsing level, Always use secure connections and secure DNS (DNS over HTTPS), and know the privacy trade-offs and when they are unavailable."
sources:
  - https://support.google.com/chrome/answer/9890866
  - https://support.google.com/chrome/answer/10468685
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Enhanced safe browsing and secure DNS

**Goal:** the browser warns about known scam and malware sites and keeps site lookups from being read on the way.

## Safe Browsing protection (Chrome)
More > Settings > **Privacy and security** > **Security**, then choose:
- **Enhanced protection:** warns about dangerous sites, downloads and extensions, even ones Google did not previously know about; Chrome sends the site URL and a small sample of page content, extension activity and system information to Google Safe Browsing, including in-depth scans of suspicious downloads. It also warns if a password was compromised in a data breach.
- **Standard protection (default):** warns about sites, downloads and extensions already identified as dangerous. Chrome sends an obfuscated portion of visited URLs through privacy servers before they reach Google, and sends full URLs and bits of page content only if a site does something suspicious.
- **No protection** is not recommended.

## HTTPS-only (Chrome)
Settings > Privacy and security > Security > under "Secure connections" turn on **Always use secure connections**. Chrome upgrades URLs to HTTPS and shows a warning before you visit a site that does not support it. You can choose to be warned for insecure public sites only, or for public and private sites (such as an intranet).

## Secure DNS (Chrome)
- Settings > Privacy and security > Security > under "Advanced", **Use secure DNS**: choose your current service provider or a custom one from the menu.
- By default secure DNS is on in automatic mode, which falls back to an unencrypted lookup if there are problems; with a custom provider Chrome does not fall back.
- Chrome says secure DNS is unavailable if the device is managed or parental controls are turned on. An error saying a server's IP address could not be found can mean a provider setting problem: check it or turn secure DNS off.

## Other browsers
Edge SmartScreen, Firefox HTTPS-Only Mode and DNS over HTTPS, and Safari's fraudulent-website warning are not covered here (see Checked).

## Verify
- [ ] Chrome shows the protection level you chose under Security, and Use secure DNS shows the provider you expect.

## Checked
2026-10-27. Chrome Help (Choose your Safe Browsing protection level; Manage Chrome safety and security) was read. Confirmed the protection levels and their data handling, the Security menu path, Always use secure connections and the secure DNS behaviour above. Edge, Firefox and Safari settings are not covered because their pages could not be confirmed. Method: documentation only; no commands were run.
