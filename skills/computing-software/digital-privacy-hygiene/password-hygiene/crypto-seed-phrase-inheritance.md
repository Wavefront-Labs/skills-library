---
id: computing-software.digital-privacy-hygiene.password-hygiene.crypto-seed-phrase-inheritance
name: crypto-seed-phrase-inheritance
category: computing-software
field: digital-privacy-hygiene
product: password-hygiene
tags: [digital-privacy-hygiene, password-hygiene, seed-phrase-inheritance, cryptocurrency, digital-legacy, shamir-backup]
level: practitioner
status: draft
description: "Plan how heirs recover self-custodied crypto using metal seed backups, Shamir or multisig splits and a letter of instruction, without exposing keys early."
sources:
  - "https://trezor.io/learn/advanced/standards-proposals/what-is-shamir-backup"
  - "https://github.com/satoshilabs/slips/blob/master/slip-0039.md"
  - "https://bitcoin.design/guide/how-it-works/private-key-management/multi-key/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Crypto wallet seed phrase inheritance

**Goal:** heirs can recover your coins after your death, but nobody (including them) can take them sooner.

## The problem
Self-custodied crypto has no "forgot password". Lose the seed phrase and passphrase and it is gone; leave them in an
obvious place and anyone can steal it.

## Building blocks
- **Metal backup** of the seed words (fire and water resistant), stored in a safe or deposit box.
- **Passphrase (25th word)** stored separately from the seed.
- **Shamir backup (SLIP-39)** on Trezor: split into shares, e.g. 2-of-3; give one to a trusted person, keep one at home,
  one in a deposit box. No single share reveals anything.
- **Multisig** (e.g. 2-of-3 with Sparrow, Nunchuk or a collaborative custody service): keys on separate hardware
  wallets; heirs need two keys plus the wallet descriptor/config file.

## Letter of instruction (not in the will)
- What wallets and assets exist, which software restores them, the derivation path or wallet descriptor.
- Where each share or key is and who holds what.
- Step-by-step recovery, written for a non-technical reader, and a warning about recovery scams.
- Exchange accounts: list them; heirs claim those through the exchange's estate process with a death certificate.

## Do not
- Put the seed in the will (public in probate), email, cloud notes or photos.
- Give one person both the seed and passphrase before it is needed.

## Test
Run a recovery drill with a small test wallet created the same way: heirs follow your instructions on a spare
device. Update after moving funds or changing wallets.
