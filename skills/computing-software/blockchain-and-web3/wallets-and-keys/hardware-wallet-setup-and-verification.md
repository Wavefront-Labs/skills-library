---
id: computing-software.blockchain-and-web3.wallets-and-keys.hardware-wallet-setup-and-verification
name: hardware-wallet-setup-and-verification
category: computing-software
field: blockchain-and-web3
product: wallets-and-keys
tags: [hardware-wallet-setup, verify-on-device, supply-chain-tamper, bc-wal-custody]
level: intro
status: draft
description: "Initialise a hardware wallet safely: buy direct, verify firmware, generate seed on device, verify addresses on screen."
sources:
  - https://support.ledger.com/
  - https://trezor.io/learn
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Hardware wallet setup
- Buy from the manufacturer or an authorised reseller; never use a pre-initialised device or one with a pre-printed seed card.
- Install firmware only via the vendor's official app; verify signatures/checksums as documented.
- Generate the seed on the device; write it by hand; do a recovery check if offered.
- Always compare the receive address and transaction details on the device screen, not the computer.
- Set a PIN; consider a passphrase for higher-value holdings (see BIP-39 caveats).
- Keep firmware updated using the vendor's process.

## Verify
- [ ] Send a small test transaction and confirm the address shown on the device equals the intended one.
