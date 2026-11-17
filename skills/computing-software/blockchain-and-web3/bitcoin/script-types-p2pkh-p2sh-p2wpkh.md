---
id: computing-software.blockchain-and-web3.bitcoin.script-types-p2pkh-p2sh-p2wpkh
name: script-types-p2pkh-p2sh-p2wpkh
category: computing-software
field: blockchain-and-web3
product: bitcoin
tags: [script-types, p2pkh, p2wpkh, bc-btc-script]
level: practitioner
status: draft
description: "Recognise P2PKH, P2SH, P2WPKH, P2WSH and P2TR outputs and their address prefixes and sizes."
sources:
  - https://developer.bitcoin.org/devguide/transactions.html
  - https://github.com/bitcoin/bips/blob/master/bip-0141.mediawiki
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Script types (mainnet)
- P2PKH: legacy, addresses start with `1`.
- P2SH: starts with `3`; wraps a script (multisig, nested segwit).
- P2WPKH: native segwit v0, bech32 `bc1q...` (short, 42 chars).
- P2WSH: native segwit script hash, `bc1q...` (62 chars).
- P2TR: taproot (segwit v1), bech32m `bc1p...`.
- Segwit spends cost fewer vbytes than legacy, so fees are lower. Prefer native segwit or taproot for new wallets.
- Identify: `bitcoin-cli getaddressinfo <addr>` and `decodescript`.

## Verify
- [ ] Decoding an address shows the expected script type and witness version.
