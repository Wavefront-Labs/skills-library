---
id: computing-software.blockchain-and-web3.bitcoin.taproot-and-schnorr-overview
name: taproot-and-schnorr-overview
category: computing-software
field: blockchain-and-web3
product: bitcoin
tags: [taproot-overview, schnorr-signatures, key-path-spend]
level: advanced
status: docs-checked
description: "Explain taproot key-path versus script-path spends and Schnorr signature benefits."
sources:
  - https://github.com/bitcoin/bips/blob/master/bip-0340.mediawiki
  - https://github.com/bitcoin/bips/blob/master/bip-0341.mediawiki
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Taproot
- BIP 340: 64-byte Schnorr signatures over secp256k1 with 32-byte (x-only) public keys.
- BIP 341: a taproot output commits to a tweaked key; spending is by key path (a single signature witness) or script path (reveals one script and proof, and the document notes that a key-path spend does not reveal whether a script path existed).
- Check wallet and hardware support before moving funds.

## Verify
- [ ] A test-wallet round trip (receive and spend to taproot) works on testnet/regtest.

## Checked

2026-11-02. Confirmed against BIP-340 (64-byte signatures, 32-byte x-only keys) and BIP-341 (key path / script path, key path hides script existence). Removed: BIP 342 tapscript detail, MuSig2, bc1p prefix, smaller witness claim (not verified on the pages read).
Method: documentation only; no commands were run.
