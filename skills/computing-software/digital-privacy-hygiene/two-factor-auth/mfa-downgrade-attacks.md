---
id: computing-software.digital-privacy-hygiene.two-factor-auth.mfa-downgrade-attacks
name: mfa-downgrade-attacks
category: computing-software
field: digital-privacy-hygiene
product: two-factor-auth
tags: [digital-privacy-hygiene, two-factor-auth, mfa-downgrade, phishing-resistant-mfa, remove-sms-recovery]
level: practitioner
status: draft
description: "Close weaker fallback factors that let attackers bypass your security key or passkey via try-another-way prompts, SMS or email recovery."
sources:
  - "https://www.cisa.gov/sites/default/files/publications/fact-sheet-implementing-phishing-resistant-mfa-508c.pdf"
  - "https://pages.nist.gov/800-63-4/sp800-63b.html"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# MFA downgrade attacks

**Goal:** an account protected by a security key is only as strong as its weakest allowed sign-in or recovery
method; remove the weak ones.

## How downgrades happen
- **"Try another way"** on the login page offers SMS, email or push alongside your key; a phishing proxy just
  picks the weak one.
- Phishing kits spoof a browser/user agent the site thinks can't do FIDO, so the site offers fallback methods.
- Account recovery by SMS or email resets everything.

## Audit each high-value account
1. List every enabled sign-in method and recovery method.
2. Remove SMS and voice; remove email codes where possible.
3. Keep: 2+ security keys/passkeys, authenticator app if you need it, printed backup codes.
4. Google: Advanced Protection removes weaker methods by design. Microsoft: passwordless removes password.
   Apple: security keys for Apple Account limit sign-in to keys plus trusted devices.

## User habit
If a site that normally asks for your key suddenly asks for an SMS code, stop: you may be on a proxy page. Check
the URL and use your password manager (it won't autofill on the wrong domain).

## Gotchas
- Some sites keep SMS silently as recovery even after you add a key; look for "recovery phone" separately.
- Leaving one authenticator-app method is a reasonable trade-off; leaving SMS usually isn't.
