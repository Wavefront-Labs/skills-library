---
id: computing-software.cryptography-implementation.protocol-implementation.encrypted-backups-for-e2ee-messaging
name: encrypted-backups-for-e2ee-messaging
category: computing-software
field: cryptography-implementation
product: protocol-implementation
tags: [protocol-implementation, cryptography-implementation, e2ee-backup, encrypted-backup, secure-value-recovery, recovery-key, e2ee]
level: sme
status: docs-checked
description: "Design E2EE messaging backups after WhatsApp's documented model: device keys, HSM vault with OPAQUE and attempt limits, 64-digit key, key hierarchy."
sources: ["https://www.whatsapp.com/security/WhatsApp_Security_Encrypted_Backups_Whitepaper.pdf", "https://support.apple.com/en-us/102651"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Encrypted backups for E2EE messaging

Backups that the provider can decrypt undo end-to-end encryption. Apple's iCloud documentation draws the line clearly: under standard data protection the keys are held in Apple data centres so Apple can help with recovery, while with end-to-end encryption (Advanced Data Protection, plus some always-E2EE categories) only trusted devices hold the keys and recovery is via device passcode or password, recovery contact or recovery key.

## Key protection choices (WhatsApp whitepaper, version of Oct 2026)
1. **Password with an HSM-enforced guess limit.** The client encrypts the backup with a random key generated on the device. That key is protected by a user password unknown to WhatsApp, cloud partners or third parties, and an encrypted version is stored in an HSM-based Backup Key Vault. The vault enforces password verification attempts and renders the key permanently inaccessible after a certain number of failed attempts. The password is registered and verified with the OPAQUE protocol, so the password is not disclosed to the vault; each login start decrements the attempt count. The vault is geographically distributed and, to tolerate two kinds of failure, deployed in seven or more datacentre sites.
2. **64-digit encryption key.** The user keeps the key; it is not sent to the vault or stored on any server. Loss means the backup cannot be recovered.
3. **Passkey.** On-device material is combined with a separate server-side key (ServerCipherKey), so neither side can derive the encryption key alone.

## Key hierarchy (first-party backup variant)
- A random 256-bit Encapsulation Key is generated on the device and protected by the chosen authentication method.
- A separate 256-bit Backup Root Key, encrypted under the Encapsulation Key with AES-256-GCM, is the root for all content and metadata keys. Because of this separation, changing the authentication method only re-runs the OPAQUE registration; the data is not re-encrypted.
- Each media file gets an independent random 256-bit key (AES-256-CBC with HMAC-SHA256, encrypt-then-MAC); each metadata envelope has its own key derived from the Backup Root Key and the file identity via HKDF (AES-256-GCM).

## Pitfalls
- Backups encrypted under keys the provider holds ("encrypted at rest" in cloud storage) are readable by the provider.
- Guess limits must be enforced by hardware or a vault, not by a client-side check.

## Checked
Method: docs-checked 2026-11-09 against the WhatsApp encrypted backups whitepaper (version 3, text extracted with pdftotext; overview, registration and login, first-party storage, key hierarchy and content encryption sections read) and the Apple iCloud data security overview page.
Removed as unconfirmed: all Signal Secure Value Recovery and secure backups claims (the cited Signal blog URL returned 404), the enclave technologies (SGX, Nitro, Azure), a "handful of attempts" figure, the HKDF/AEAD/AAD generic design rules, advice on not backing up identity keys and safety-number changes, rotation on PIN change, and incremental chunk-key backups.
