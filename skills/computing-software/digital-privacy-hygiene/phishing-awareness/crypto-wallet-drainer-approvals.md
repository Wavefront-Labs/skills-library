---
id: computing-software.digital-privacy-hygiene.phishing-awareness.crypto-wallet-drainer-approvals
name: crypto-wallet-drainer-approvals
category: computing-software
field: digital-privacy-hygiene
product: phishing-awareness
tags: [digital-privacy-hygiene, phishing-awareness, wallet-drainer, credential-phishing, exchange-withdrawal-allowlist]
level: practitioner
status: draft
description: "Avoid wallet drainer scams: dangerous approval and permit signatures, fake mint and airdrop sites, transaction simulation, and revoking token approvals."
sources:
  - "https://revoke.cash/learn/approvals/what-are-token-approvals"
  - "https://etherscan.io/tokenapprovalchecker"
  - "https://support.metamask.io/stay-safe/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Crypto wallet drainer approvals

**Goal:** never sign the transaction or message that lets a scammer empty your wallet.

## How drainers work
Fake mint, airdrop-claim, "wallet verification" or support sites ask you to connect and sign:
| Signature | Risk |
|---|---|
| `approve` / `increaseAllowance` with huge amount | Spender can move that token any time |
| `setApprovalForAll` | Spender can move all NFTs in a collection |
| `permit` / Permit2 (off-chain typed data) | Gasless approval; looks like "just a signature" |
| Seed phrase request | Total loss; legit apps never ask |

## Defences
- Wallet with **transaction simulation** and warnings (built-in security alerts in major wallets, or Rabby).
- Hardware wallet with clear signing; read what you sign.
- A **burner wallet** with small funds for mints and new dapps; main funds in a separate wallet.
- Bookmark real dapp URLs; avoid links from DMs, replies and search ads.

## Review and revoke approvals
revoke.cash or Etherscan's Token Approval Checker: connect (read-only), list approvals, revoke unknown or unlimited
ones (costs gas).

## If drained
- Revoke remaining approvals, move what's left to a **new wallet with a new seed** if the seed may be exposed.
- Report to the platform/IC3; beware "recovery services", which are scams.

## Gotchas
- Off-chain permit signatures don't show as transactions until used.
- Discord/X "support" DMs are scams; real support doesn't DM first.
