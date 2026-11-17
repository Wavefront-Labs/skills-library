---
id: computing-software.digital-privacy-hygiene.device-hardening.picocrypt-file-encryption
name: picocrypt-file-encryption
category: computing-software
field: digital-privacy-hygiene
product: device-hardening
tags: [digital-privacy-hygiene, device-hardening, picocrypt, file-encryption, argon2id, xchacha20]
level: practitioner
status: draft
description: "Encrypt individual files or folders with Picocrypt: password and keyfile options, paranoid mode, Reed-Solomon error correction, and verifying downloads."
sources:
  - "https://github.com/Picocrypt/Picocrypt"
  - "https://www.privacyguides.org/en/encryption/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Picocrypt file encryption

**Goal:** a small, portable tool to encrypt a file or folder with a password before storing or sending it.

## What it is
Open-source, single small executable for Windows, macOS and Linux. Uses XChaCha20 with Argon2id key derivation and
HMAC/BLAKE2 authentication; no installation, no account. Privacy Guides has listed it as a file encryption option.
Check the repository's current maintenance status and use a maintained release before adopting it long term.

## Encrypt
1. Drag files or a folder onto the window (folders are zipped first).
2. Enter a strong passphrase (or generate one), or add **keyfiles** (any file, optionally required in order).
3. Options:
   - **Paranoid mode**: cascade with Serpent and stronger Argon2 parameters; slower.
   - **Reed-Solomon**: adds error correction so minor corruption on old media can be repaired.
   - **Split** into chunks for upload limits.
   - **Deniability** hides the volume header so the file looks like random data.
4. Click Encrypt; output is a `.pcv` file. Delete the original securely if it should not remain.

## Decrypt
Drop the `.pcv` file in, enter the password and keyfiles. Picocrypt verifies integrity and warns if the file was
modified or damaged ("Force decrypt" exists for recovery; treat the output with suspicion).

## Good practice
- Send the password through a different channel than the file.
- Keyfiles are as critical as the password: back them up separately.
- Verify the download's checksum/signature from the GitHub release.

## Alternatives
age (CLI, public-key friendly), 7-Zip AES-256 with encrypted file names, VeraCrypt containers for many files,
Cryptomator for cloud folders.
