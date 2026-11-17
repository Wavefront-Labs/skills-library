---
id: computing-software.cloud-infrastructure-engineering.saltstack.salt-key-fingerprints-and-signing
name: salt-key-fingerprints-and-signing
category: computing-software
field: cloud-infrastructure-engineering
product: saltstack
tags: [saltstack, salt-key, fingerprint, gen-keys, gen-signature, master-signing, keysize]
level: advanced
status: docs-checked
description: "Print key fingerprints, generate keypairs, and sign the Salt master public key with salt-key --gen-signature so minions can verify it."
sources:
  - https://raw.githubusercontent.com/saltstack/salt/master/doc/ref/cli/salt-key.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# salt-key fingerprints, keypairs and signing

Fingerprints: `-f <key>` prints one key's fingerprint; `-F` prints all.

Keypair generation:
- `--gen-keys <name>`: name of the generated pair.
- `--gen-keys-dir <dir>`: output directory (default: current directory).
- `--keysize <bits>`: default and minimum 2048.

Master public key signing:
- `--gen-signature` creates a `master_pubkey_signature` file for the master's public key; a minion can use it to verify the master's key cryptographically.
- `--priv`: private key used to sign.
- `--pub`: public key to sign.
- `--signature-path`: where to write the signature file.
- `--auto-create`: create a signing keypair if none exists.

## Checked

2026-11-04: read the salt-key CLI reference page in full. Confirmed -f and -F, --gen-keys, --gen-keys-dir (default current directory), --keysize (default 2048, smaller rounded up), --gen-signature and its companion options. Nothing removed.

Method: documentation only; no commands were run.

