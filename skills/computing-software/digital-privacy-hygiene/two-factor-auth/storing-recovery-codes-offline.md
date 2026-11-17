---
id: computing-software.digital-privacy-hygiene.two-factor-auth.storing-recovery-codes-offline
name: storing-recovery-codes-offline
category: computing-software
field: digital-privacy-hygiene
product: two-factor-auth
tags: [digital-privacy-hygiene, two-factor-auth, offline-recovery-sheet, backup-codes, recovery-codes, look-up-secrets, emergency-kit, nist-800-63b, fireproof-storage]
level: intro
status: draft
description: "Keep 2FA recovery codes where they survive losing every device but not where a burglar or malware finds them: a printed recovery sheet plus a vault copy for low-value accounts."
sources:
  - "https://pages.nist.gov/800-63-4/sp800-63b.html"
  - "https://support.google.com/accounts/answer/1187538"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Storing recovery codes offline

**Goal:** recovery codes (NIST "look-up secrets" / saved recovery codes) are a full
bypass of your 2FA. Store them as carefully as the 2FA itself, and away from it.

## Where they should go
| Account class | Storage |
|---|---|
| Vault, primary email, Apple/Google/Microsoft account | **Printed sheet** in a home safe or sealed envelope, second copy off-site (trusted relative, safe deposit box) |
| Bank, carrier, registrar, GitHub | Printed sheet; optionally also an encrypted file outside the vault |
| Everything else | In the password manager item's hidden field or attachment is fine |

Never: in the same authenticator app, in the email account they protect, in plain
notes, or as a screenshot in a cloud photo library.

## Recovery sheet format
One page, handwritten or printed from an offline machine:
```
RECOVERY SHEET - updated 2026-10-16
Google (alice@...)        8 codes: xxxx xxxx ...  (used: 0)
Bitwarden recovery code   xxxx-xxxx-...
Apple recovery key        XXXX-XXXX-...
```
Cross out codes as you use them, and regenerate when half are used (see
`computing-software.digital-privacy-hygiene.two-factor-auth.regenerating-backup-codes-after-use`).

## Printing safely
Printers with storage or cloud print services may retain jobs; prefer a basic USB
printer or handwriting. Delete the downloaded `.txt` file and empty the trash.

## Gotchas
- A fire takes the home copy; the off-site copy is the point.
- Mark the envelope neutrally ("Household documents"), not "PASSWORDS".

## Verify
- [ ] Two physical copies in separate locations, dated.
- [ ] No recovery code text files left in Downloads or cloud drives.
