---
id: computing-software.digital-privacy-hygiene.password-hygiene.auditing-the-account-recovery-chain
name: auditing-the-account-recovery-chain
category: computing-software
field: digital-privacy-hygiene
product: password-hygiene
tags: [digital-privacy-hygiene, password-hygiene, recovery-chain-audit, primary-email-security, recovery-email, recovery-phone, account-takeover, reset-graph, circular-dependency]
level: practitioner
status: draft
description: "Map which email and phone can reset each important account, find weak links (old addresses, partner phones, circular recovery), and fix them."
sources:
  - "https://support.google.com/accounts/answer/183723"
  - "https://www.privacyguides.org/en/basics/email-security/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Auditing the account recovery chain

**Goal:** an attacker attacks the weakest account in the chain, not the strongest. If
your bank resets via an old Yahoo address with a reused password, the bank's strength
doesn't matter.

## Build the graph (30 minutes)
For each of: password manager, primary email(s), Apple/Google/Microsoft, carrier, bank,
brokerage, social, registrar:
- Recovery **email**: which address?
- Recovery **phone**: which number? whose?
- Other recovery: codes, trusted contacts, security questions.
Draw arrows: `Bank -> gmail A -> recovery: yahoo B -> recovery phone (old number)`.

## Weak links to look for
- Old/abandoned emails (ISP, university, work) as recovery addresses.
- Recovery numbers that are old, landlines, or belong to an ex/parent.
- **Circular dependencies**: email A recovers via email B, B via A, both locked if you lose
  the phone. Fine if each also has a backup method (codes/keys); fatal if not.
- Recovery accounts with weaker protection than the account they recover.
- Email aliases services as recovery for the alias service itself.

## Fix
- Every recovery email must be one you actively use, with MFA at least as strong as the
  account it recovers.
- Remove numbers you don't control.
- Add offline recovery codes so no chain depends solely on one device.

## Verify
- [ ] Diagram written down (in the vault) with no abandoned addresses or foreign numbers.
- [ ] Each node has MFA and an offline recovery method.
