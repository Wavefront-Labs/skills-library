---
id: computing-software.digital-privacy-hygiene.two-factor-auth.splitting-recovery-secrets-with-trusted-people
name: splitting-recovery-secrets-with-trusted-people
category: computing-software
field: digital-privacy-hygiene
product: two-factor-auth
tags: [digital-privacy-hygiene, two-factor-auth, secret-sharing-escrow, digital-legacy, emergency-kit]
level: practitioner
status: draft
description: "Split a critical recovery secret among trusted people using Shamir secret sharing or simple envelope schemes so no single holder can use it."
sources:
  - "https://manpages.debian.org/testing/ssss/ssss.1.en.html"
  - "https://github.com/satoshilabs/slips/blob/master/slip-0039.md"
  - "https://ssd.eff.org/module/your-security-plan"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Splitting recovery secrets with trusted people

**Goal:** heirs or co-trustees can recover your master password or seed phrase together, but no one person can.

## Options
| Method | Security | Complexity |
|---|---|---|
| Whole secret in one sealed envelope with an attorney | Trust in one party | Low |
| Two halves of the passphrase to two people | Each half leaks half the entropy; weak | Low |
| **Shamir secret sharing** (k of n) | Fewer than k shares reveal nothing | Medium |
| SLIP-39 (crypto wallets, e.g. Trezor) | Shamir with wordlists and checksums | Medium |

## Shamir with ssss (offline machine)
```
ssss-split -t 2 -n 3        # threshold 2 of 3 shares; paste secret when prompted
ssss-combine -t 2           # paste any 2 shares to recover
```
Print each share with a label ("share 1 of 3, threshold 2, tool ssss") and instructions on how to combine.

## Distribution
- Give shares to people who don't all live together and are unlikely to collude (spouse, sibling, attorney).
- Write recovery instructions separately: which tool, where to find it, what the secret unlocks.
- Test recovery once with dummy data in front of the holders.

## Gotchas
- Tools change; include the tool name and version, or keep a copy of the tool on a USB stick with the instructions.
- Never split a secret by halves of characters; use real secret sharing.
- Revoke by changing the underlying secret, then redistribute.
