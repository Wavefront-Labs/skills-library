---
id: computing-software.cryptography-implementation.protocol-implementation.ssh-key-types-and-generation
name: ssh-key-types-and-generation
category: computing-software
field: cryptography-implementation
product: protocol-implementation
tags: [cryptography-implementation, protocol-implementation, ssh, openssh, ssh-keygen, ed25519, ed25519-sk, fido2, rsa-sha2-512, passphrase, bcrypt-kdf]
level: practitioner
status: docs-checked
description: "Generate SSH keys well: Ed25519 vs ed25519-sk (FIDO2) vs RSA, passphrase KDF rounds, resident keys, comments, and retiring ssh-rsa (SHA-1) and DSA keys."
sources: ["https://raw.githubusercontent.com/openssh/openssh-portable/master/ssh-keygen.1", "https://www.openssh.com/txt/release-10.0", "https://www.openssh.com/txt/release-7.8", "https://www.openssh.com/txt/release-8.2", "https://www.openssh.com/txt/release-8.8", "https://datatracker.ietf.org/doc/html/rfc8709"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SSH key types and generation

## Choose the type

| Type | Use | Notes |
|---|---|---|
| `ed25519` | default for users and hosts | Small, fast, RFC 8709 |
| `ed25519-sk` / `ecdsa-sk` | hardware-backed (FIDO/U2F security key) | Key material stays on the token; touch required unless `no-touch-required` (OpenSSH 8.2+) |
| `rsa` (3072+) | only for old servers/appliances | Use with `rsa-sha2-256/512` signatures |
| `ecdsa` (P-256) | where Ed25519 is unsupported | |
| `dsa` | never | Support removed in OpenSSH 10.0 |

```bash
ssh-keygen -t ed25519 -a 100 -C "alice@laptop-2026" -f ~/.ssh/id_ed25519
ssh-keygen -t ed25519-sk -O resident -O verify-required -C "alice@yubikey" -f ~/.ssh/id_ed25519_sk
ssh-keygen -t rsa -b 4096 -a 100 -f ~/.ssh/id_rsa_legacy
```

- `-a 100`: bcrypt_pbkdf KDF rounds protecting the private key file with the
  passphrase (the current ssh-keygen(1) documents a default of 32; older releases
  used fewer). Higher = slower brute force of a stolen key file.
  OpenSSH's own private key format is the default since 7.8.
- Always set a passphrase for user keys and use `ssh-agent` - or use `-sk` keys.
- `-O resident` stores the key handle on the token so `ssh-keygen -K` can
  recover it on a new machine; `verify-required` demands PIN plus touch.

## SHA-1 deprecation of "ssh-rsa"

OpenSSH 8.8 disabled the `ssh-rsa` **signature algorithm** (RSA with SHA-1)
by default. RSA keys still work with `rsa-sha2-256/512`. Old servers that only
speak `ssh-rsa` fail; temporary client override per host:

```
Host legacy-box
    HostKeyAlgorithms +ssh-rsa
    PubkeyAcceptedAlgorithms +ssh-rsa
```

Fix the server instead (upgrade, or add an Ed25519 host key).

## Inspect and convert

```bash
ssh-keygen -lf ~/.ssh/id_ed25519.pub          # fingerprint (SHA256:...)
ssh-keygen -y -f ~/.ssh/id_ed25519            # public key from private
ssh-keygen -p -a 100 -f ~/.ssh/id_rsa         # change passphrase / upgrade KDF rounds
ssh-keygen -e -m PKCS8 -f key.pub             # export public key for other tools
```

## Verify

- [ ] No DSA keys; RSA keys >= 3072 bits (`ssh-keygen -lf` shows size).
- [ ] Private key files encrypted (`ssh-keygen -y -f` prompts for the passphrase).
- [ ] High-value access uses `-sk` keys or certificates.

## Checked

2026-10-31. Confirmed in the current ssh-keygen(1) source (`-a rounds` is the bcrypt_pbkdf round count and the default is 32; RSA
default 3072 bits; `-t` types ecdsa, ecdsa-sk, ed25519, ed25519-sk, rsa; `-K`, `-y`, `-p`, `-e`, `PKCS8` export, `resident`,
`verify-required`, `rsa-sha2-256/512`), the OpenSSH 8.2 notes (`ecdsa-sk`, `ed25519-sk`), 8.8 notes (RSA/SHA-1 `ssh-rsa`
signatures disabled by default; the `+ssh-rsa` stop-gap example), 7.8 notes (OpenSSH private key format by default),
10.0 notes (DSA support removed) and RFC 8709 (Ed25519 in SSH). Corrected: the default for `-a` was written as 16.
Removed (no source read): `aes256-ctr` header check, `ssh-add -t 8h` and `AddKeysToAgent yes`, the "some FIPS systems"
remark for ECDSA.
Method: documentation only; no commands were run.
