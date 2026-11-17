---
id: computing-software.digital-privacy-hygiene.privacy-configuration.compartmentalizing-usernames-and-personas
name: compartmentalizing-usernames-and-personas
category: computing-software
field: digital-privacy-hygiene
product: privacy-configuration
tags: [digital-privacy-hygiene, privacy-configuration, username-compartmentalization, digital-footprint, osint, personas, email-aliases, pseudonymity]
level: practitioner
status: draft
description: "Use different usernames, emails and avatars per life context so accounts cannot be linked, and audit existing handle reuse with OSINT tools like WhatsMyName."
sources:
  - "https://whatsmyname.app/"
  - "https://ssd.eff.org/module/how-to-manage-your-digital-footprint"
  - "https://www.privacyguides.org/en/basics/account-creation/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Compartmentalizing usernames and personas

**Goal:** one reused handle lets anyone pivot from your gaming account to your real name, employer and home.
Break the links.

## Audit current reuse
- Run your handles and email addresses through **WhatsMyName** (whatsmyname.app) or Sherlock
  (`sherlock myhandle`) to see every site where the same username exists.
- Reverse image search your avatars (Google Lens, TinEye, PimEyes for faces); reused profile photos link accounts
  as strongly as names.
- Check breach data (Have I Been Pwned) for old handles tied to your email.

## Design personas
| Persona | Name/handle | Email | Photo |
|---|---|---|---|
| Professional | Real name | Work or main address | Headshot |
| Personal/social | Variation, friends-only | Personal alias | Different photo |
| Interests/forums/gaming | Unrelated handle per community | Alias per site (SimpleLogin/addy.io/Hide My Email) | Non-photo avatar |
| Anonymous/sensitive | Unique handle, never reused | Dedicated alias or separate provider | None |

## Keep them apart
- Generate handles randomly (password manager username generator) rather than variations of a theme.
- Never cross-link profiles, follow your own personas, or reuse bios, phrasing and in-jokes.
- Watch metadata: time zone of posting, photos with EXIF, phone number verification shared across accounts.
- Use separate browser profiles or containers per persona; store each in a tagged password manager folder.

## Retire old handles
Delete or rename dormant accounts using an old linked handle; request search engine removal of cached profiles.

## Verify
- [ ] WhatsMyName search for your main handle shows only accounts you intend to be linked.
- [ ] Sensitive persona shares no handle, email, phone or photo with the others.
