---
id: computing-software.digital-privacy-hygiene.password-managers.uri-match-detection-as-a-phishing-check
name: uri-match-detection-as-a-phishing-check
category: computing-software
field: digital-privacy-hygiene
product: password-managers
tags: [digital-privacy-hygiene, password-managers, uri-match-detection, autofill-as-phishing-check, autofill, password-autofill, base-domain, lookalike-domains, phishing, credential-phishing]
level: practitioner
status: draft
description: "Configure URI match rules so autofill only offers credentials on the real domain, and treat 'no suggestion' as a phishing alarm instead of copy-pasting the password."
sources:
  - "https://bitwarden.com/help/uri-match-detection/"
  - "https://support.1password.com/autofill/"
  - "https://ssd.eff.org/module/how-avoid-phishing-attacks"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# URI match detection as a phishing check

**Goal:** make the password manager your best anti-phishing tool: it compares the
domain exactly, which humans can't do reliably under pressure.

## How matching works (Bitwarden names; others similar)
| Mode | Matches | Use for |
|---|---|---|
| Base domain (default) | `example.com` and any subdomain | Most sites |
| Host | exact hostname and port | Shared hosting, `*.github.io`, different apps on subdomains |
| Starts with | URL prefix | One path on a multi-tenant domain |
| Exact | whole URL | Rare |
| Regular expression | regex | Advanced; easy to get wrong |
| Never | nothing | Items you never want auto-suggested |

Set it per URI on an item, or change the default in Settings > Autofill.

## Fix the matches you have
- Sites with separate login domains (`login.microsoftonline.com`, `accounts.google.com`,
  a bank's auth domain): add the extra URI to the item **after verifying it from the
  real site's own redirect**, never from a link in an email.
- Multi-tenant hosts (`*.azurewebsites.net`, `*.github.io`, `*.myshopify.com`): use
  **Host** so one tenant's lookalike doesn't get your credentials.
- iOS/Android apps: add the `androidapp://` or associated-domain entries the manager
  offers when you first fill in an app.

## The rule that stops phishing
**If the manager doesn't offer the login, stop.** Do not search the vault and paste.
Check the address bar: lookalikes (`rnicrosoft.com`), punycode (`xn--`), and extra
labels (`paypal.com.verify-account.io`) are exactly what base-domain matching rejects.
Only add a new URI after you've reached the site by typing the address or via a
bookmark.

## Gotchas
- Organisations sometimes legitimately move login to a new domain; the first time is
  the riskiest. Confirm via the provider's status/help page.
- Autofill does not protect against a compromised legitimate site or AitM proxies
  on the real-looking domain; pair with passkeys/security keys.

## Verify
- [ ] Visit a lookalike test (e.g. your bank's domain with a typo, without logging in):
      no suggestion appears.
- [ ] Household members know "no suggestion = don't paste".
