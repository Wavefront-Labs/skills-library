---
id: computing-software.digital-privacy-hygiene.password-managers.equivalent-domains-and-match-rules
name: equivalent-domains-and-match-rules
category: computing-software
field: digital-privacy-hygiene
product: password-managers
tags: [digital-privacy-hygiene, password-managers, equivalent-domains, uri-match-detection, autofill]
level: practitioner
status: draft
description: "Configure equivalent domains and per-item URI match rules so logins fill across a company's domains without matching attacker lookalikes."
sources:
  - "https://bitwarden.com/help/uri-match-detection/"
  - "https://bitwarden.com/help/domain-rules/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Equivalent domains and match rules

**Goal:** make one saved login work on `example.com`, `example.co.uk` and `exampleapp.com` without creating
rules loose enough to fill on `example-login.top`.

## Bitwarden domain rules
Settings > Domain rules (web vault):
- **Global equivalent domains:** curated groups (e.g. Google properties, Apple domains, Microsoft domains).
  Exclude any group you don't want.
- **Custom equivalent domains:** add a comma-separated set you control, e.g. `example.com, example.co.uk`.

## Per-item URI match detection
Each URI on a login can use: Base domain (default), Host, Starts with, Exact, Regular expression, Never.
| Situation | Choose |
|---|---|
| Different logins per subdomain (`git.corp.com` vs `mail.corp.com`) | Host |
| Router or NAS on an IP and port | Host (includes port) or Exact |
| Never fill this page (e.g. a change-password page with wrong fields) | Never |
| Many tenant subdomains on a SaaS (`acme.slack.com`) | Host for your tenant |

Avoid Regular expression unless you anchor it (`^https://login\.example\.com/`); an unanchored regex can match
attacker URLs that contain the string.

## Multiple URIs on one item
Add every legit domain to the item (Edit > New URI) instead of global equivalence when only one account needs it.

## Gotchas
- Base domain uses the public suffix list: `user.github.io` sites are separate, which is correct.
- Changing the default match for the whole vault (Settings > Auto-fill) affects every item; prefer per-item.

## Verify
On each legit domain the item appears as a match; on a lookalike domain it does not.
