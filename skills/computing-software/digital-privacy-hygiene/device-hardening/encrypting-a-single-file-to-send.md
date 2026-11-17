---
id: computing-software.digital-privacy-hygiene.device-hardening.encrypting-a-single-file-to-send
name: encrypting-a-single-file-to-send
category: computing-software
field: digital-privacy-hygiene
product: device-hardening
tags: [digital-privacy-hygiene, device-hardening, age-encryption, encrypted-archive, file-encryption, 7-zip-aes, gpg-symmetric, password-out-of-band, zipcrypto]
level: practitioner
status: draft
description: "Encrypt one file before emailing or uploading it: age (public key or passphrase), gpg symmetric, or a 7-Zip AES-256 archive with encrypted file names, password sent separately."
sources:
  - "https://github.com/FiloSottile/age"
  - "https://www.privacyguides.org/en/encryption/"
  - "https://www.7-zip.org/7z.html"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Encrypting a single file to send

**Goal:** send a tax return, ID scan or contract through email/cloud links without the
mail provider or a later breach exposing it.

## Option 1: age (simple, modern)
```bash
# recipient generates a key once and sends you the public key (age1...)
age-keygen -o key.txt
# encrypt to their public key
age -r age1qyqszqgpqyqszqgpqyqszqgpqyqszqgpqyqszqgp... -o tax.pdf.age tax.pdf
# or with a passphrase (prompts)
age -p -o tax.pdf.age tax.pdf
# decrypt
age -d -i key.txt -o tax.pdf tax.pdf.age
```
Also encrypts to SSH public keys (`-R ~/.ssh/id_ed25519.pub`).

## Option 2: gpg symmetric
```bash
gpg --symmetric --cipher-algo AES256 tax.pdf      # creates tax.pdf.gpg
gpg --output tax.pdf --decrypt tax.pdf.gpg
```

## Option 3: 7-Zip archive (for non-technical recipients)
7-Zip > Add to archive > format **7z** > Encryption method **AES-256** > tick **Encrypt
file names** > password. Command line:
```bash
7z a -t7z -mhe=on -p tax.7z tax.pdf
```
Recipients on macOS can use Keka or The Unarchiver.

## Password delivery
Send the passphrase via a **different channel** (phone call, Signal). A random 4-5 word
passphrase is strong and easy to dictate.

## Gotchas
- Legacy **ZIP "ZipCrypto"** encryption is broken; Windows built-in zip can't create AES
  zips. Use 7z/AES-256.
- Office/PDF "password to open" varies in strength by version; don't rely on old formats.
- Delete plaintext temp copies after sending.

## Verify
- [ ] Recipient decrypted successfully; passphrase never sent in the same channel.
