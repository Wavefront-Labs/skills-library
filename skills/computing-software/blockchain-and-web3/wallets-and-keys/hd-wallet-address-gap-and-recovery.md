---
id: computing-software.blockchain-and-web3.wallets-and-keys.hd-wallet-address-gap-and-recovery
name: hd-wallet-address-gap-and-recovery
category: computing-software
field: blockchain-and-web3
product: wallets-and-keys
tags: [gap-limit, wallet-recovery, derivation-path-mismatch]
level: practitioner
status: draft
description: "Recover a wallet on a new device, handle the gap limit and diagnose empty-looking restores."
sources:
  - https://github.com/bitcoin/bips/blob/master/bip-0044.mediawiki
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Recovery
- Wallets scan addresses until `gap limit` (commonly 20) consecutive unused addresses. If you generated more than that without using them, funds beyond the gap may not show: raise the gap limit and rescan.
- If a restore shows zero: check the passphrase, the derivation path / script type (legacy, nested, native segwit, taproot) and the coin type.
- Try restoring in watch-only mode first so no secret touches a risky device.
- Keep a record of wallet software, version, derivation path and script type with the backup (not the seed itself in the same place).

## Verify
- [ ] The restored wallet balance equals the balance before the test.
