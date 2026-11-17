---
id: computing-software.blockchain-and-web3.wallets-and-keys.bip32-derivation-paths
name: bip32-derivation-paths
category: computing-software
field: blockchain-and-web3
product: wallets-and-keys
tags: [bip32-derivation, bip44-paths, xpub-privacy]
level: advanced
status: docs-checked
description: "Derive keys from a master seed using BIP-32 paths and understand what an extended public key reveals."
sources:
  - https://github.com/bitcoin/bips/blob/master/bip-0032.mediawiki
  - https://github.com/bitcoin/bips/blob/master/bip-0044.mediawiki
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Derivation
- BIP-44 path: `m / purpose' / coin_type' / account' / change / address_index`. The apostrophe marks hardened derivation.
- BIP-32: an extended public key `(K, c)` can derive child public keys, but only non-hardened ones; hardened children need the private key. Mainnet extended keys encode as `xprv`/`xpub` (testnet `tprv`/`tpub`).
- Treat an xpub as sensitive: it exposes the non-hardened child public keys.
- Specific coin_type values, BIP-84/86 paths, tool names and the xpub-plus-child-private-key leak: not covered by the pages read; look them up in the BIPs and the SLIP-44 registry.

## Verify
- [ ] Derived key from a known test vector matches the BIP document.

## Checked

2026-11-02. Confirmed against BIP-32 (CKDpub only for non-hardened, xprv/xpub/tprv/tpub prefixes, test vectors) and BIP-44 (path format). Removed: coin_type values (0, 60), BIP-84 and BIP-86 paths, tool/library names, the parent-key recovery claim, wallet-default-path remark (not on the pages read).
Method: documentation only; no commands were run.
