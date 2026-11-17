---
id: computing-software.cryptography-implementation.crypto-libraries.age-recipient-types-and-plugins
name: age-recipient-types-and-plugins
category: computing-software
field: cryptography-implementation
product: crypto-libraries
tags: [crypto-libraries, cryptography-implementation, age-plugin, age, file-encryption, x25519, yubikey, post-quantum]
level: practitioner
status: gated
description: "Use age encryption recipient types and plugins: X25519, SSH, scrypt passphrase, post-quantum hybrid recipients, YubiKey and TPM plugins, and recipient file handling."
sources: ["https://github.com/FiloSottile/age", "https://github.com/FiloSottile/age/releases/tag/v1.3.0", "https://c2sp.org/age", "https://c2sp.org/age-plugin", "https://github.com/str4d/age-plugin-yubikey", "https://github.com/FiloSottile/awesome-age"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# age recipient types and plugins

## Built-in recipients
```sh
age-keygen -o key.txt                          # X25519 identity, prints age1... recipient
age -r age1abc... -o f.age f                   # encrypt to recipient
age -R recipients.txt -o f.age f               # many recipients, one per line
age -R ~/.ssh/id_ed25519.pub -o f.age f        # SSH ed25519 or RSA public key
age -p -o f.age f                              # passphrase (scrypt), cannot mix with other recipients
age -d -i key.txt f.age > f
```
age 1.3.0 adds post-quantum recipients: HPKE with a hybrid ML-KEM-768 KEM, generated with `age-keygen -pq`; recipients start `age1pq1...` and identities `AGE-SECRET-KEY-PQ-1...`. Older clients can use the optional `age-plugin-pq` (`age-plugin-pq -identity` converts hybrid identities). The CLI also accepts `age1tag1...`/`age1tagpq1...` recipients (compatible with hardware plugins; the 1.3.0 notes say the latest or upcoming age-plugin-yubikey, -tpm and -se will support them). `age-inspect` shows whether a file uses PQ encryption. For a file to be PQ-safe all its recipients must be PQ.

Checked with age 1.3.2 (windows-amd64 release): `age-keygen -o`, `-r`, `-R` with a recipients file, `-R` with an `ssh-ed25519` and an `ssh-rsa` public key and `-i` with the matching private key, `age-keygen -pq` (recipient `age1pq1...`, identity `AGE-SECRET-KEY-PQ-1...`) and a PQ round trip all decrypted to the original text; `age-inspect` reported `"mlkem768x25519"` and `This file uses post-quantum encryption` (1627-byte header) for the PQ file and `"X25519"` and `does NOT use post-quantum encryption` (168-byte header) for the classic one; `age -p -r ...` stops with `-p/--passphrase can't be combined with -r/--recipient`. The v1.3.2 release archive also contains `age-plugin-pq`, `age-plugin-tag`, `age-plugin-tagpq` and `age-plugin-batchpass` (non-interactive passphrases, with a warning in its man page).

## Plugins (age-plugin spec)
- Recipients `age1<name>1...` and identities `AGE-PLUGIN-<NAME>-1...` call a binary `age-plugin-<name>` on PATH.
- Common (listed in awesome-age and the age README): `age-plugin-yubikey` (PIV slot, touch/PIN policy), `age-plugin-tpm`,
  `age-plugin-se` (Apple Secure Enclave), `age-plugin-fido2-hmac`. The YubiKey flags below come from that plugin's README;
  no YubiKey was available to run them (gated: unconfirmed, source is paywalled or blocked).
```sh
age-plugin-yubikey --generate --touch-policy cached
age -r age1yubikey1q... -o secret.age secret
age -d -i yubikey-identity.txt secret.age
```

## Operational notes
- Encrypt to at least two recipients (hardware key plus offline backup key) to avoid lockout.
- age has no signatures; pair with minisign or ssh-keygen -Y sign for authenticity.
- Recipient files are public; identity files are secrets (encrypt them with a passphrase: `age -p key.txt`).

## Verify
- [ ] Decrypt test with each recipient identity, including the backup key, before deleting plaintext.
