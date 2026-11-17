---
id: computing-software.digital-privacy-hygiene.password-managers.username-and-email-alias-generation
name: username-and-email-alias-generation
category: computing-software
field: digital-privacy-hygiene
product: password-managers
tags: [digital-privacy-hygiene, password-managers, username-generator, password-generator, email-aliases, simplelogin, addy-io, firefox-relay, plus-addressing, catch-all-email, unlinkability]
level: practitioner
status: draft
description: "Generate a unique username and email alias per account from the password manager, so a breach at one site can't be joined to your other accounts."
sources:
  - "https://bitwarden.com/help/generator/"
  - "https://www.privacyguides.org/en/email-aliasing/"
  - "https://simplelogin.io/docs/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Username and email alias generation

**Goal:** a unique password stops credential stuffing; a unique **email and
username** also stops cross-site correlation, targeted phishing and data-broker
linking.

## Options, weakest to strongest
| Method | Example | Weakness |
|---|---|---|
| Plus addressing | `you+shop@gmail.com` | Trivially stripped; reveals real address |
| Catch-all on own domain | `shop@yourdomain.tld` | Domain links all aliases to you; spam to any name |
| Random word on own domain | `velvet.otter42@yourdomain.tld` | Domain still links them |
| Forwarding alias service | SimpleLogin, addy.io, Firefox Relay, DuckDuckGo, Fastmail masked email | Service sees mail; but aliases are unlinkable from outside and can be disabled individually |

## Bitwarden generator
Generator > **Username** type:
- **Plus addressed email** or **Catch-all email** (enter your domain).
- **Forwarded email alias**: choose service (SimpleLogin, addy.io, Firefox Relay,
  Fastmail, DuckDuckGo, ForwardEmail) and paste that service's API key. The generator
  creates a real alias via the API and puts it in the username field.
- **Random word** username (with optional number) for sites that want a handle.
1Password integrates Fastmail Masked Email similarly.

## Workflow per new account
1. Open the manager's new-item flow on the signup page.
2. Generate alias, then password, save the item **before** submitting the form (so a
   failed submit doesn't lose the alias).
3. Note the alias in the item; it is now the login identifier too.

## Gotchas
- Banks and government sites may later require a "real" email for statements; aliases
  still work but some block known alias domains. Use your own domain to avoid this.
- If the alias provider dies, you lose password resets. Use a custom domain with the
  alias service so you can move providers.
- Replying from an alias needs the provider's reverse-alias feature, or you leak your
  real address.

## Verify
- [ ] Three most recent signups each have a distinct alias and username.
- [ ] You can disable one alias without affecting others.
