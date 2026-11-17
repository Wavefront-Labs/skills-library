---
id: computing-software.cryptography-implementation.applied-cryptography.openssh-post-quantum-key-exchange
name: openssh-post-quantum-key-exchange
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [applied-cryptography, cryptography-implementation, sntrup761, mlkem768x25519, openssh, ssh, post-quantum, kexalgorithms, hybrid-kem, pq-migration]
level: practitioner
status: docs-checked
description: "Enable and verify post-quantum key exchange in OpenSSH (mlkem768x25519-sha256, sntrup761x25519-sha512), handle old peers and PQ warnings."
sources: ["https://www.openssh.com/pq.html", "https://www.openssh.com/releasenotes.html", "https://man.openbsd.org/sshd_config#KexAlgorithms"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OpenSSH post-quantum key exchange

## Versions
| OpenSSH | PQ default |
|---|---|
| 9.0 (2022) | `sntrup761x25519-sha512@openssh.com` default |
| 9.9 | adds `mlkem768x25519-sha256` |
| 10.0 | `mlkem768x25519-sha256` becomes the default |
| 10.1 | ssh warns when a connection does not use a PQ key exchange (disable with `WarnWeakCrypto` in ssh_config) |

## Check what you negotiate
```
ssh -Q kex | grep -E "mlkem|sntrup"
ssh -v user@host 2>&1 | grep "kex: algorithm"
```

## Configure
Server (`/etc/ssh/sshd_config`) and client (`~/.ssh/config`):
```
KexAlgorithms mlkem768x25519-sha256,sntrup761x25519-sha512,curve25519-sha256
```
Keep a classical fallback until every peer supports a PQ method; remove it once logs show no classical negotiations.
Check whether a distribution-wide crypto policy overrides the list before editing the file.

## Peers that lag
- Servers older than 9.0 offer no PQ method; 9.0 to 9.8 offer only sntrup761x25519-sha512. Upgrade, or check that
  `KexAlgorithms` has not disabled the PQ methods (the OpenSSH PQ page's advice for the 10.1 warning).
- Appliances and non-OpenSSH SSH libraries may lack PQ KEX; check each.
- PQ KEX protects session confidentiality against store-now-decrypt-later attacks.

## Verify
- [ ] `ssh -v` shows a PQ kex algorithm to every managed host.
- [ ] ssh 10.1 or later prints no post-quantum warning when connecting to each managed host.

## Checked
2026-11-01. Confirmed against the OpenSSH post-quantum page, the release notes (9.0, 9.9, 10.0, 10.1) and the sshd_config manual (WarnWeakCrypto). Removed the nmap check, the libssh alias, crypto-policy and Go library claims (not in the fetched pages).
Method: documentation only; no commands were run.
