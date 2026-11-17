---
id: computing-software.digital-privacy-hygiene.password-hygiene.verbal-passwords-with-banks-and-carriers
name: verbal-passwords-with-banks-and-carriers
category: computing-software
field: digital-privacy-hygiene
product: password-hygiene
tags: [digital-privacy-hygiene, password-hygiene, verbal-password, security-questions, phone-banking, carrier-account-pin, port-out-pin, social-engineering, call-centre-verification]
level: intro
status: draft
description: "Set a verbal password or account PIN with your bank, mobile carrier and utilities so phone agents can't be talked into changes by someone who knows your public details."
sources:
  - "https://www.fcc.gov/sim-swap-port-out-fraud"
  - "https://consumer.ftc.gov/articles/what-know-about-identity-theft"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Verbal passwords with banks and carriers

**Goal:** the phone channel is the weakest link: agents verify with name, address, date
of birth and last four of an SSN, all of which leak in breaches. A verbal password adds
something that isn't public.

## Where to set one
| Organisation | What it's called | How |
|---|---|---|
| Mobile carrier | Account PIN / passcode, plus separate **port-out / number transfer PIN** | Carrier app security settings or store visit |
| Bank / card issuer | Verbal password, telephone banking passcode, "security word" | Call, secure message, or branch |
| Utilities, ISP | Account password/PIN | Account settings |
| Credit bureaus | Freeze PIN / account password | Bureau account |

## Choosing it
- Random two or three words (`velvet harbour tango`): easy to say, not guessable.
- Different for each organisation; store as a hidden custom field in the vault item.
- Not a fact about you, not your phone passcode.

## Using it
- When **you** call: offer it up front.
- When **they** call you: never give it. Hang up and call the number on your card or bill
  (scammers pose as fraud departments to harvest exactly this).

## Gotchas
- Some agents skip it if you "forgot"; ask the organisation to flag the account so that a
  failed verbal password triggers extra checks.
- Family members on the account need to know theirs or the account holder's process.

## Verify
- [ ] Carrier, main bank and email-provider-billing accounts have a verbal password/PIN set.
- [ ] Each is stored in the vault and differs.
