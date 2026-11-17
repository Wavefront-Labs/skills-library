---
id: computing-software.digital-privacy-hygiene.phishing-awareness.entered-a-password-on-a-phishing-page
name: entered-a-password-on-a-phishing-page
category: computing-software
field: digital-privacy-hygiene
product: phishing-awareness
tags: [digital-privacy-hygiene, phishing-awareness, credential-compromise-response, phishing-incident-response, revoke-sessions, email-forwarding-rules, password-reuse, account-takeover]
level: intro
status: draft
description: "Step-by-step response after typing a password (and maybe a 2FA code) into a phishing page: change it, kill sessions, check rules and recovery, and cover reused passwords."
sources:
  - "https://www.cisa.gov/secure-our-world/recognize-and-report-phishing"
  - "https://consumer.ftc.gov/articles/how-recognize-and-avoid-phishing-scams"
  - "https://support.google.com/accounts/answer/6294825"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Entered a password on a phishing page

**Goal:** act within minutes; attackers using live phishing kits log in immediately with
your password and code.

## Immediately (from a trusted device, typing the real address)
1. **Change the password** of that account to a new unique one.
2. **Sign out all sessions**: Google Security > Your devices > sign out; Microsoft "Sign
   out everywhere"; Meta Accounts Center > Where you're logged in; others in security
   settings. This kills stolen session cookies.
3. If you also entered a 2FA code, assume the attacker is in: check **security info**
   (added phone/email/authenticator? remove), and **recovery** details.
4. Email accounts: check **forwarding rules and filters** (attackers add rules to hide or
   forward mail), connected apps, app passwords, and **sent** items.

## Within the hour
- Same password used elsewhere? Change it there too (start with email, bank).
- Turn on MFA (better: passkey/security key) if not already.
- Tell your contacts if the account sent messages (phishing spreads from hijacked accounts).
- Work account: report to IT immediately; they can revoke tokens centrally.
- Financial account: call the provider's fraud line.

## Afterwards
- Report the phishing page (browser "Report deceptive site", the provider's abuse address).
- Watch for follow-up phishing using what they learned.

## Verify
- [ ] Password changed, sessions revoked, no unknown recovery methods or forwarding rules.
- [ ] All accounts sharing that password updated.
