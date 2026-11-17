---
id: computing-software.systems-network-administration.cisco-networking.local-users-with-scrypt-secrets
name: local-users-with-scrypt-secrets
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, ios-xe, algorithm-type-scrypt, type-9-password, type-8-password, enable-secret, username-secret, password-hashing, password-encryption-aes]
level: practitioner
status: draft
description: "Create IOS local users and enable secrets with type 9 (scrypt) or type 8 hashes, migrate off type 5/7, and manage hashes in templates safely."
sources:
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/security/d1/sec-d1-cr-book/sec-cr-u1.html
  - https://sec.cloudapps.cisco.com/security/center/resources/ios_password_types.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Local users with algorithm-type scrypt

## Password types
| Type | Algorithm | Status |
|---|---|---|
| 0 | plaintext | never |
| 7 | Vigenere obfuscation (`service password-encryption`) | reversible in seconds |
| 4 | broken SHA-256 implementation | deprecated, removed |
| 5 | MD5-crypt | legacy, crackable |
| 8 | PBKDF2-SHA-256 | good |
| 9 | scrypt | recommended |

## Configure
```
enable algorithm-type scrypt secret <ENABLE_SECRET>
username netadmin privilege 15 algorithm-type scrypt secret <PASSWORD>
username readonly privilege 1 algorithm-type sha256 secret <PASSWORD>    ! type 8
```
Resulting config: `username netadmin privilege 15 secret 9 $9$...`. Paste that exact hash into
templates instead of the plaintext: `username netadmin privilege 15 secret 9 $9$abc...`.

## Migrating
- Find weak entries: `show running-config | include password|secret 5|secret 7`.
- `username x password ...` stores type 0/7: replace with `secret`.
- Older IOS (pre-15.3(3)) lacks types 8/9; upgrade or keep type 5 as an interim.
- `password encryption aes` + `key config-key password-encrypt` protects other stored secrets
  (type 6) such as RADIUS/TACACS keys and ISAKMP keys.

## Gotchas
- Typing `enable secret 9 <plaintext>` is rejected; the `9` means "following is a hash".
- Downgrading to an IOS without scrypt support makes type 9 users unusable: keep a console path.
- Hashes in configs in Git are still sensitive (offline cracking); protect the repo.

## Verify
- [ ] `show run | include secret` shows only types 8/9 for users and enable.
- [ ] No `username ... password` lines remain.
