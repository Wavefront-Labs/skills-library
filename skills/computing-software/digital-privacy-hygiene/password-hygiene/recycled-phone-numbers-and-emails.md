---
id: computing-software.digital-privacy-hygiene.password-hygiene.recycled-phone-numbers-and-emails
name: recycled-phone-numbers-and-emails
category: computing-software
field: digital-privacy-hygiene
product: password-hygiene
tags: [digital-privacy-hygiene, password-hygiene, phone-number-recycling, recovery-chain-audit, account-recovery]
level: practitioner
status: draft
description: "Handle phone numbers and email addresses that get recycled to new owners: update accounts before giving them up, and check accounts tied to old numbers."
sources:
  - "https://www.cs.princeton.edu/~arvindn/publications/recycled-phone-numbers.pdf"
  - "https://www.fcc.gov/consumers/guides/porting-keeping-your-phone-number-when-you-change-providers"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Recycled phone numbers and email addresses

**Goal:** the next person to get your old number or address can't reset your accounts or read your codes.

## The risk
Carriers reassign disconnected numbers, often within weeks to months. Research (Princeton, 2021) found many
recycled numbers still received SMS codes and password resets for previous owners' accounts. Some free email
providers recycle inactive addresses too (e.g. after long inactivity).

## Before giving up a number
1. Build a list of accounts using it: search your password manager for the number, check major accounts' security
   settings, banks, carriers, social media.
2. Change the number on each account (or remove phone entirely), starting with email and financial accounts.
3. Keep the old number alive briefly (cheap prepaid plan) to catch missed accounts via incoming codes. Or port it to
   a VoIP service to keep it long term.

## Before abandoning an email address
- Update every account's login/recovery email.
- Set an auto-reply only if you trust the provider not to recycle; otherwise keep logging in to keep it active.

## After getting a new number
You may receive codes for strangers; don't use them. Expect spam for the previous owner.

## Check old ties
Use "forgot password" on major services with the old number/email: if it finds an account, update it.

## Gotchas
- Inactive Google accounts can be deleted after 2 years of inactivity; keep recovery emails on active accounts.
- Messaging apps (WhatsApp, Signal) keyed to phone numbers: re-register on the new number and delete the old.
