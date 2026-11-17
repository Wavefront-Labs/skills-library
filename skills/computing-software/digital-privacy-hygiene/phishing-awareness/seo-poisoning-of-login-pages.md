---
id: computing-software.digital-privacy-hygiene.phishing-awareness.seo-poisoning-of-login-pages
name: seo-poisoning-of-login-pages
category: computing-software
field: digital-privacy-hygiene
product: phishing-awareness
tags: [digital-privacy-hygiene, phishing-awareness, seo-poisoning, malvertising, credential-phishing, bookmarks]
level: practitioner
status: draft
description: "Avoid fake login and support pages that rank in search results or ads, using bookmarks, password manager URL matching and domain checks."
sources:
  - "https://www.cisa.gov/news-events/news/avoiding-social-engineering-and-phishing-attacks"
  - "https://www.ic3.gov/Media/Y2022/PSA221221"
  - "https://bitwarden.com/help/uri-match-detection/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# SEO poisoning of login pages

**Goal:** never type credentials into a lookalike site that came from a search result.

## How it works
Attackers buy search ads or game rankings for queries like "Chase login", "MetaMask download", "Coinbase support
number". The result looks official, but the domain is a lookalike (`chase-secure-login.com`, an extra letter, a
Unicode homoglyph) and the page steals credentials, 2FA codes or installs malware. The FBI warned about search ad
impersonation in 2022, and it continues.

## Habits
1. **Bookmarks or typed addresses** for banking, email, crypto and work portals; never search for them.
2. **Password manager autofill as a check:** if the manager doesn't offer to fill on a page you think is your bank,
   stop and read the URL.
3. **Skip ads:** sponsored results sit on top; scroll past them for account sites. An ad blocker hides most.
4. **Read the domain right to left**: `login.bank.com.evil.io` belongs to `evil.io`.
5. **Support numbers:** get them from the back of your card or the app, never from search results.
6. **Passkeys** cannot be used on the wrong domain, removing this whole class of attack.

## If you entered credentials
Change the password from a bookmark, revoke sessions, check recovery methods; see the incident skill for phished
passwords.
