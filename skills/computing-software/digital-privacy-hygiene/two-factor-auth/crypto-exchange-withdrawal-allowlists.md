---
id: computing-software.digital-privacy-hygiene.two-factor-auth.crypto-exchange-withdrawal-allowlists
name: crypto-exchange-withdrawal-allowlists
category: computing-software
field: digital-privacy-hygiene
product: two-factor-auth
tags: [digital-privacy-hygiene, two-factor-auth, exchange-withdrawal-allowlist, security-keys, sim-swap]
level: practitioner
status: draft
description: "Harden a crypto exchange account: security key 2FA, withdrawal address allowlist with time lock, anti-phishing code, and no SMS fallback."
sources:
  - "https://help.coinbase.com/en/coinbase/privacy-and-security/account-security/address-book"
  - "https://support.kraken.com/hc/en-us/articles/360000426923"
  - "https://www.ftc.gov/business-guidance/blog/2022/06/new-data-shows-ftc-received-2400-percent-increase-crypto-scam-reports"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Crypto exchange withdrawal allowlists

**Goal:** even with your password and a session, an attacker can't send funds to their address.

## Controls to enable (names vary by exchange)
| Control | Effect |
|---|---|
| Security key / passkey 2FA | Phishing-resistant login and withdrawal approval |
| Remove SMS 2FA and phone recovery | Defeats SIM-swap takeovers, the classic exchange theft |
| **Withdrawal address allowlist** (address book allowlisting) | Withdrawals only to pre-approved addresses |
| Delay on new addresses (24-72 h hold) | Time to notice and lock the account |
| Settings/global lock | Changes to security settings require a waiting period |
| Anti-phishing code | Exchange emails include your code; missing code = fake email |
| API keys | Withdraw permission off; IP-restricted |

## Procedure
1. Add security keys, then remove SMS.
2. Add your own wallet addresses to the address book, verify each by sending a small test amount.
3. Turn on allowlisting; confirm the hold period.
4. Enable the anti-phishing code.
5. Review active sessions and API keys.

## If something looks wrong
Use the exchange's "disable account"/freeze option first (often a link in emails or a support page), then
change passwords from a clean device.

## Gotchas
- Allowlists only help if adding an address requires 2FA and a delay.
- Long-term holdings belong in self-custody hardware wallets, not on exchanges.
