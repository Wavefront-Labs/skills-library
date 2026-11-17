---
id: computing-software.blockchain-and-web3.wallets-and-keys.operational-security-for-key-holders
name: operational-security-for-key-holders
category: computing-software
field: blockchain-and-web3
product: wallets-and-keys
tags: [crypto-opsec, phishing-defence, clipboard-address-check]
level: intro
status: draft
description: "Reduce theft risk from phishing, malicious approvals, clipboard malware and fake support using concrete habits."
sources:
  - https://ethereum.org/en/security/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Operational security (defensive)
- Bookmark official sites; do not follow links from DMs or ads. No legitimate support will ask for your seed phrase.
- Dedicated browser profile or device for wallet use; minimal extensions.
- Read what you sign: transaction summary, spender, amount, and especially unlimited token approvals and blind `setApprovalForAll`/permit signatures.
- Review and revoke old token approvals periodically with a reputable approvals tool.
- Verify full addresses, not just first/last characters (address poisoning sends lookalike dust to pollute history).
- Keep large holdings in cold storage, a separate hot wallet for daily use.

## Verify
- [ ] You can list the approvals your hot wallet currently has outstanding and justify each.
