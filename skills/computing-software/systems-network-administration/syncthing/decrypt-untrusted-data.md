---
id: computing-software.systems-network-administration.syncthing.decrypt-untrusted-data
name: decrypt-untrusted-data
category: computing-software
field: systems-network-administration
product: syncthing
tags: [syncthing, decrypt, untrusted, recovery]
level: advanced
status: docs-checked
description: "Recover plaintext from an encrypted Syncthing folder with syncthing decrypt, using --to, --verify-only and FOLDER_PASSWORD."
sources: ["https://docs.syncthing.net/users/untrusted.html", "https://docs.syncthing.net/users/syncthing.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Decrypting untrusted folder data

## When
You recovered a backup or lost the Syncthing database on an untrusted device and need the plaintext data. The command converts the encrypted data to plaintext on disk, so run it only on a trusted device. It does not depend on Syncthing running; it works on offline data.

## Command
```sh
syncthing decrypt --to /path/to/plaintext --password <folder-password> /path/to/encrypted-folder
```
Point it at the root of the encrypted folder.

## Options
- `--to=<dir>` destination for decrypted files.
- `--verify-only` checks plaintext hashes without writing files.
- `--password=<pw>` or the `FOLDER_PASSWORD` environment variable, which avoids leaving the secret in shell history or the process list.
- `--folder-id=<id>` if it cannot be found automatically.
- `--token-path=<file>` token file inside the folder, used to find the folder ID.
- `--continue` keeps going after an error rather than aborting.

## Notes
The data is encrypted using both the password and the folder ID. The folder ID is normally stored in the folder marker, but the docs advise storing both securely and reliably. Encryption is XChaCha20-Poly1305 and AES-SIV with a key derived from the password and folder ID using scrypt.

## Checked
2026-11-04. Read Untrusted (Encrypted) Devices and Command Line Operation (decrypt options): command form, the recovery scenario, `--to`, `--verify-only`, `--password`/`FOLDER_PASSWORD`, `--folder-id`, `--token-path`, `--continue`, key inputs and ciphers. Removed the claim that `--verify-only` is a cheap password check, which the pages do not state.
Method: documentation only; no commands were run.
