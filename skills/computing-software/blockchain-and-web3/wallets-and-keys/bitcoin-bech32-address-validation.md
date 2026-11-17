---
id: computing-software.blockchain-and-web3.wallets-and-keys.bitcoin-bech32-address-validation
name: bitcoin-bech32-address-validation
category: computing-software
field: blockchain-and-web3
product: wallets-and-keys
tags: [bech32-validation, bech32m, address-format-check]
level: practitioner
status: draft
description: "Validate Bitcoin addresses (base58check, bech32, bech32m) and network prefixes before sending."
sources:
  - https://github.com/bitcoin/bips/blob/master/bip-0173.mediawiki
  - https://github.com/bitcoin/bips/blob/master/bip-0350.mediawiki
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Bitcoin address validation
- Base58Check (legacy `1...`, `3...`): payload + 4-byte double-SHA256 checksum.
- Bech32 (BIP 173) for segwit v0 (`bc1q`); bech32m (BIP 350) for v1+ (`bc1p` taproot). Using the wrong checksum constant makes the address invalid.
- Prefixes: mainnet `bc1`, testnet `tb1`, regtest `bcrt1`; mixed-case is invalid in bech32.
- Validate with `bitcoin-cli validateaddress <addr>` or a well-tested library; do not write your own regex-only validator.
- Reject addresses of the wrong network in applications.

## Verify
- [ ] Known-good and one-char-altered addresses are accepted and rejected respectively.
