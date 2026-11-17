---
id: computing-software.digital-privacy-hygiene.password-managers.autofill-on-page-load-and-clickjacking-risk
name: autofill-on-page-load-and-clickjacking-risk
category: computing-software
field: digital-privacy-hygiene
product: password-managers
tags: [digital-privacy-hygiene, password-managers, autofill-on-page-load, autofill-clickjacking, autofill, password-autofill, browser-extension, inline-menu, xss, extension-updates]
level: practitioner
status: draft
description: "Keep autofill user-initiated: disable fill-on-page-load, understand DOM clickjacking of extension menus, and keep the extension patched."
sources:
  - "https://bitwarden.com/help/auto-fill-browser/"
  - "https://support.1password.com/autofill/"
  - "https://owasp.org/www-community/attacks/Clickjacking"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Autofill on page load and clickjacking

**Goal:** credentials should be filled only when you deliberately ask, on a page you
deliberately chose.

## Why fill-on-page-load is risky
If the manager fills as soon as a matching page loads, any script on that page
(an XSS bug, a malicious third-party script, an injected ad iframe on a compromised
subdomain that still matches **base domain**) can read the filled fields without you
doing anything. Invisible forms can harvest credentials as you browse.

## Settings
- **Bitwarden**: Settings > Autofill > "Autofill on page load" **off** (it is off by
  default and carries a warning). Prefer the inline menu or keyboard shortcut
  (`Ctrl/Cmd+Shift+L`).
- **1Password**: fills on click/shortcut; keep "Show autofill menu on field focus"
  only if you understand the next section.
- **KeePassXC-Browser**: keep "Automatically fill in single-credential entries" off for
  sensitive entries; use the key icon or `Ctrl+Shift+U`.

## Clickjacking of extension UI
Researchers (presented publicly in 2025) showed that many manager extensions' in-page
dropdowns could be made transparent or overlaid by a malicious page, so a click on an
innocent-looking element actually selected "fill" for card, identity or login data.
Mitigations:
- Update extensions promptly; vendors shipped fixes at different speeds. Check the
  extension's version and changelog after such disclosures.
- Where available, disable the **inline menu on field focus** and use the toolbar
  popup or keyboard shortcut, which page content cannot overlay.
- Don't keep card and identity items set to auto-suggest everywhere; restrict them.
- Uncertain: which vendors fully fixed which variants changes over time; verify your
  extension's current status.

## Gotchas
- "Fill on load" also breaks your phishing alarm: you stop noticing whether the
  manager recognised the site.
- Subdomain takeover on a domain you trust makes base-domain matching fill on an
  attacker page; use Host matching for high-value logins.

## Verify
- [ ] Opening a saved login page fills nothing until you act.
- [ ] Extension version checked against the vendor's latest.
