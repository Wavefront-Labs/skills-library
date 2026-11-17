---
id: computing-software.digital-privacy-hygiene.password-hygiene.handling-account-lockout
name: handling-account-lockout
category: computing-software
field: digital-privacy-hygiene
product: password-hygiene
tags: [digital-privacy-hygiene, password-hygiene, account-lockout, rate-limiting, credential-stuffing]
level: practitioner
status: docs-checked
description: "Respond to being locked out after failed attempts: wait out throttling, recover safely, and treat unexplained lockouts as a sign someone is guessing."
sources:
  - "https://pages.nist.gov/800-63-4/sp800-63b.html"
  - "https://owasp.org/www-community/controls/Blocking_Brute_Force_Attacks"
  - "https://www.ncsc.gov.uk/collection/passwords/updating-your-approach"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Account lockout after failed attempts

**Goal:** get back in without making it worse, and know when a lockout means an attack.

## Why sites lock or slow you down
- NIST SP 800-63B-4 section 3.2.2 requires verifiers to limit consecutive failed attempts on one authenticator on an
  account to no more than 100 by disabling it; that is an upper bound and operators may set lower limits. A disabled
  authenticator must be rebound to the account before use. The text asks that users be told how many attempts remain
  and how long to wait.
- The UK NCSC prefers throttling (progressively increasing delay between attempts) to lockout. If a service locks out,
  it suggests allowing 5 to 10 attempts first. Real limits vary by service, so read the site's own message.
- OWASP notes lockout can be abused to deny service by locking many accounts, and does not stop slow attacks or one
  password tried against many usernames.

## If you locked yourself out
1. **Stop retrying.** Further attempts may extend a delay or keep an account locked. Wait for the time the service states.
2. Look in the password manager for the saved password rather than guessing variations.
3. Use the service's official recovery flow, then update the vault.
4. Keep recovery methods current in advance: lockout needs an account recovery route (NCSC).

## If you didn't cause it
An unexpected lockout or "too many attempts" message may mean someone is guessing passwords for your account. The NCSC
lists unexpected account lockouts as an indicator security teams monitor for, alongside brute-forcing and password
spraying and failed second-step MFA.
- Change the password if it was reused anywhere, and make it unique.
- Turn on multi-factor authentication where the service supports it (the NCSC recommends MFA for important accounts).
- If you are in an organisation, report it to IT or security so they can check the logs.

## Gotchas
- Lockout of an account you share (service accounts, family logins) hits everyone using it.
- Device PINs, SIM PINs and security keys have their own lock rules set by the maker or carrier; check their
  documentation before experimenting.

## Checked
Confirmed 2026-11-08 against NIST SP 800-63B-4 (rate limiting, section 3.2.2), the OWASP Blocking Brute Force Attacks
page and the NCSC updating-your-approach guidance. The account.live.com source returned an empty sign-in redirect and
was dropped. Removed: the "growing delays, CAPTCHAs" description attributed to NIST, "often 15 minutes to 24 hours",
the iPhone and Android behaviour, the Have I Been Pwned step, the Microsoft alias advice, and PUK and YubiKey details,
none of which the readable pages state.
Method: docs-only read of cited pages, 2026-11-08
