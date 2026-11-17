---
id: computing-software.blockchain-and-web3.wallets-and-keys.bip39-mnemonic-seed-handling
name: bip39-mnemonic-seed-handling
category: computing-software
field: blockchain-and-web3
product: wallets-and-keys
tags: [bip39-mnemonic, seed-phrase-backup, passphrase-25th-word, bc-wal-hd]
level: practitioner
status: draft
description: "Explain how a BIP-39 mnemonic derives the seed, what the optional passphrase does and how to back it up safely."
sources:
  - https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# BIP-39
- Entropy (128-256 bits) plus a checksum is encoded as 12-24 words from a 2048-word list. Seed = PBKDF2-HMAC-SHA512 of the mnemonic with salt "mnemonic" + optional passphrase, 2048 rounds.
- The passphrase ("25th word") creates a completely different wallet; a wrong passphrase gives a valid-looking empty wallet. Losing it means losing the funds.
- Backup: write words on durable media (metal), store in separate secure places, never photograph or type into cloud notes or websites.
- Generate only on trusted hardware or well-reviewed offline software.
- Wordlist language and derivation differ between wallets using non-BIP-39 schemes (for example Electrum's own seed format); do not assume interchange.

## Verify
- [ ] Restore the seed on a second, offline device with a tiny test balance and confirm the same first address.
