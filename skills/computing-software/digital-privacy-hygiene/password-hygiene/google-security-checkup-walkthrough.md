---
id: computing-software.digital-privacy-hygiene.password-hygiene.google-security-checkup-walkthrough
name: google-security-checkup-walkthrough
category: computing-software
field: digital-privacy-hygiene
product: password-hygiene
tags: [digital-privacy-hygiene, password-hygiene, google-security-checkup, primary-email-security, revoke-sessions]
level: practitioner
status: draft
description: "Walk through Google Security Checkup item by item: devices, recent activity, sign-in and recovery, third-party access, Gmail settings and saved passwords."
sources:
  - "https://myaccount.google.com/security-checkup"
  - "https://support.google.com/accounts/answer/46526"
  - "https://support.google.com/accounts/answer/3466521"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Google Security Checkup walkthrough

**Goal:** a 10-minute review of the Google account that probably resets half your other accounts.

## Open
myaccount.google.com/security-checkup (or Google app > Manage your Google Account > Security > Security issues).

## Sections and what to do
| Section | Action |
|---|---|
| Your devices | Sign out any device you don't recognise or no longer own |
| Recent security activity | Investigate new sign-ins, recovery changes, password changes you didn't make |
| Sign-in & recovery | Recovery phone current, recovery email you control, 2-Step Verification on with passkey/security key |
| Third-party access | Remove apps you don't use; especially ones with Gmail or Drive access |
| Gmail settings | Check forwarding and filters that forward or delete mail (common attacker persistence) |
| Saved passwords | Password Checkup: compromised, reused, weak (if you use Google Password Manager) |
| Enhanced Safe Browsing | Optional; sends more data to Google for better phishing protection |

## Extra checks not always shown
- Gmail > Settings > See all settings > Forwarding and POP/IMAP: no unknown forwarding address.
- Gmail > Filters and Blocked Addresses: no filter deleting security emails.
- myaccount.google.com > Security > App passwords: remove old ones.

## Cadence
After any phishing scare, after losing a device, and every 3-6 months.

## Gotchas
- Google may mark everything green while weak recovery (old phone number) remains; read the details.
- Signing out a device doesn't revoke an app password or OAuth token; remove those separately.
