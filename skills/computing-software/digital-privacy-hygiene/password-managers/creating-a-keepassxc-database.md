---
id: computing-software.digital-privacy-hygiene.password-managers.creating-a-keepassxc-database
name: creating-a-keepassxc-database
category: computing-software
field: digital-privacy-hygiene
product: password-managers
tags: [digital-privacy-hygiene, password-managers, kdbx-database-creation, keepassxc, kdf]
level: practitioner
status: docs-checked
description: "Create a KeePassXC database with KDBX 4 and Argon2id, tune the decryption time, choose credentials, and store the file where it syncs and backs up."
sources:
  - "https://keepassxc.org/docs/KeePassXC_UserGuide#_creating_your_first_database"
  - "https://keepassxc.org/docs/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Creating a KeePassXC database

**Goal:** a new KDBX vault whose key derivation makes offline guessing expensive, unlocks acceptably on your
slowest device, and won't be lost.

## Steps
1. Open KeePassXC and click the create new database button. Enter a name and an optional description.
2. **Encryption Settings:** the guide recommends changing nothing except the **Decryption Time** slider. A higher
   value gives more protection and a longer open time. Encryption time depends on hardware; the guide says a
   mobile device will likely take two to four times longer than a home computer, so test there before raising it.
3. **Database Credentials:** enter a long, randomized password (the password generator button helps). Losing the
   password can lock the database permanently. Optionally add a key file or a YubiKey/OnlyKey challenge-response.
4. Click Done and choose where to save the `.kdbx` file. The guide says the file is fully encrypted at all times,
   so it can be stored in cloud storage (OneDrive, Dropbox, Google Drive, Nextcloud, Syncthing); prefer a service
   that keeps version history, and make sure nothing deletes the file by accident.

## Advanced Settings (only if you know what they mean)
The **Advanced Settings** checkbox on the encryption screen exposes the key derivation function:
- **Argon2** (KDBX 4, recommended): memory-hard, so more resistant to GPU/ASIC attacks than AES-KDF. Raising the
  memory parameter makes attacks harder and the time longer; parallelism sets the thread count. The guide recommends
  **Argon2id** to guard against timing-based attacks; Argon2d gives maximum compatibility with other KeePass apps.
- **AES-KDF** works with KDBX 4 and 3.1; KDBX 3.1 supports only AES-KDF, so Argon2 needs KDBX 4.

## Later changes
Database > Database Settings lets you change the password and add or remove credentials (key file, YubiKey
challenge-response) and the encryption settings.

## Gotchas
- A lost key file or hardware key can lock you out as surely as a forgotten password; back them up. The guide has a
  section on creating a YubiKey backup.
- Test the database on every device and client you use before relying on it.

## Checked
2026-11-01. Confirmed in the KeePassXC User Guide (creating a database, storing it, Database Settings, advanced
key derivation). Removed: default of about 1 second, 2-3 s and 64-256 MiB figures, the 6-word diceware advice,
AES-256 vs ChaCha20 statement, client names, Syncthing-as-recommendation wording, "Database Settings shows KDBX 4"
verify step.
Method: documentation only; no commands were run.
