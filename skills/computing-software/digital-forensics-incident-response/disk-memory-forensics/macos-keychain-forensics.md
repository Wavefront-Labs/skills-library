---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.macos-keychain-forensics
name: macos-keychain-forensics
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [keychain-forensics, macos-keychain, chainbreaker, credential-artefacts, macos-forensics, dfir]
level: advanced
status: draft
description: "Examine macOS keychains: login and System keychain files, the data-protection keychain, metadata readable without a password, decryption with chainbreaker, and theft indicators."
sources: ["https://github.com/n0fate/chainbreaker", "https://support.apple.com/guide/security/keychain-data-protection-secb0694df1a/web", "https://attack.mitre.org/techniques/T1555/001/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# macOS keychain forensics

Keychains hold saved passwords, Wi-Fi keys, certificates, private keys and app tokens. Investigators examine them to establish which accounts a user had, whether credentials were present for systems the attacker accessed, and whether the keychain itself was stolen (T1555.001).

## Files
- Login keychain: `~/Library/Keychains/login.keychain-db` (encrypted with the user's login password by default).
- System keychain: `/Library/Keychains/System.keychain` (key in `/private/var/db/SystemKey`).
- Data-protection (iCloud-style) keychain: `~/Library/Keychains/<UUID>/keychain-2.db` (SQLite), protected by keybag classes tied to the Secure Enclave on T2/Apple Silicon; generally not decryptable offline.

## Without the password
The legacy `.keychain-db` format exposes metadata in clear: item class, service/server names, account names, creation and modification dates, labels. That alone shows which services the user saved credentials for and when. chainbreaker can dump this metadata:
```bash
python -m chainbreaker --dump-all --output out/ login.keychain-db
```

## With authorisation and a credential
With the user's password (or a recovered master key from memory, or the SystemKey for the System keychain), chainbreaker decrypts generic and internet passwords, private keys and certificates:
```bash
python -m chainbreaker --dump-all --password-prompt login.keychain-db
python -m chainbreaker --dump-all --key-prompt System.keychain   # key from SystemKey
```
Handle decrypted output as highly sensitive evidence; decrypt only what the authorisation covers.

## Live system
`security dump-keychain -a` lists items and access control; `security find-generic-password -s <service>` (prompts for access). Unified logs record `securityd`/`secd` access prompts; repeated prompts or `security` tool use by unusual parents (Terminal launched by a malicious app) indicate theft attempts. Infostealers (Atomic, MetaStealer) copy `login.keychain-db` and phish the password with a fake dialog.

## Indicators of theft
- `login.keychain-db` accessed or copied by a non-Apple process (EDR file events, ESF).
- Archives in temp folders containing keychain files; outbound uploads right after.
- osascript dialogs asking for the password (unified log, `osascript` process with `display dialog ... hidden answer`).

## Gotchas
- Apple Silicon and T2 Macs: data-protection keychain items are hardware-bound; image the live system or work from iCloud via legal process.
- Changing the login password without the old one leaves the old keychain locked; a "login keychain reset" creates a new file and renames the old one.

## Verify
Report which keychain files were examined, whether decryption was performed and under what authority, and keep metadata-only findings distinct from decrypted findings.
