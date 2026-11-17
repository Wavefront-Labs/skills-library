---
id: computing-software.cryptography-implementation.protocol-implementation.ssh-key-revocation-lists
name: ssh-key-revocation-lists
category: computing-software
field: cryptography-implementation
product: protocol-implementation
tags: [protocol-implementation, cryptography-implementation, ssh-krl, openssh, revokedkeys, ssh-certificates, key-revocation, ssh-keygen]
level: practitioner
status: docs-checked
description: "Revoke SSH user keys and certificates with OpenSSH KRLs: ssh-keygen -k specs by serial, key id, key and hash, RevokedKeys in sshd, and testing with -Q."
sources: ["https://man.openbsd.org/ssh-keygen#KEY_REVOCATION_LISTS", "https://man.openbsd.org/sshd_config#RevokedKeys"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SSH key revocation lists

## Create a KRL
`revoke.spec`:
```
serial: 1024-1030
id: alice@example.com
key: ssh-ed25519 AAAAC3Nza... bob-old-laptop
hash: SHA256:Hx7b...                       # by SHA256 fingerprint
```
```
ssh-keygen -k -f /etc/ssh/revoked.krl -s user_ca.pub revoke.spec      # new KRL; -s scopes serial/id lines to this CA
ssh-keygen -k -u -f /etc/ssh/revoked.krl -s user_ca.pub more.spec     # update existing
ssh-keygen -Q -f /etc/ssh/revoked.krl ~/.ssh/id_ed25519-cert.pub      # test: non-zero exit if revoked or on error
```
The `serial:` and `id:` directives need the CA key given with `-s`. Serial numbers are 64-bit, nonzero, and may be
a range (`1024-1030`). `key:` revokes a plain public key (a certificate listed there is revoked as a plain key);
`hash:` takes a SHA256 fingerprint and `sha256:` a public key, and KRLs using SHA256 hashes need OpenSSH 7.9 or later.
The `-z` flag on `-k` sets a KRL version number, not a certificate serial.

## sshd
```
RevokedKeys /etc/ssh/revoked.krl
```
`RevokedKeys` names a revoked-keys file (a text file of public keys or a KRL) or `none`. Deploy the file to every host
before enabling the option and test how your sshd version behaves if it is missing.

## Operations
- Distribute the KRL to every host via config management.
- Revoke by certificate serial (assign unique serials when signing: `ssh-keygen -s ca -z <serial>`) or key id for
  people.
- Short-lived SSH certificates (hours) reduce the need for KRLs; still keep a KRL for emergencies.

## Verify
- [ ] `ssh-keygen -Q` on a revoked certificate exits non-zero, and login with it is refused.
- [ ] Every host has the current KRL (check its hash).

## Checked

2026-11-01: ssh-keygen(1) KEY REVOCATION LISTS and signing synopsis, and sshd_config(5) RevokedKeys, read. Confirmed: -k, -u, -Q, -s, spec directives and their meanings, 7.9 note for SHA256 hashes, RevokedKeys values. Corrected: sha256 vs hash directive; -z on -k is a KRL version. Removed: fail-closed claim, binary-size claim, log message, host-key revocation via known_hosts or ssh_config.
Method: documentation only; no commands were run.
