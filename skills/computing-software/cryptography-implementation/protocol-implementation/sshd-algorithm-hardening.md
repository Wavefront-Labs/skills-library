---
id: computing-software.cryptography-implementation.protocol-implementation.sshd-algorithm-hardening
name: sshd-algorithm-hardening
category: computing-software
field: cryptography-implementation
product: protocol-implementation
tags: [cryptography-implementation, protocol-implementation, ssh, openssh, ssh-hardening, kexalgorithms, mlkem768x25519, sntrup761x25519, ciphers, macs, ssh-audit, terrapin]
level: advanced
status: docs-checked
description: "Harden OpenSSH algorithm settings: PQ hybrid KEX (mlkem768x25519, sntrup761x25519), AEAD ciphers, ETM MACs, host key algorithms, Terrapin mitigation, and auditing with ssh-audit."
sources: ["https://man.openbsd.org/sshd_config", "https://www.openssh.com/txt/release-9.9", "https://terrapin-attack.com/", "https://github.com/jtesta/ssh-audit"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# sshd algorithm hardening

Current OpenSSH defaults are good; hardening mostly means removing legacy
algorithms kept for compatibility and preferring post-quantum key exchange.

## Recommended (OpenSSH 9.9+)

```
# /etc/ssh/sshd_config.d/50-crypto.conf
KexAlgorithms mlkem768x25519-sha256,sntrup761x25519-sha512,sntrup761x25519-sha512@openssh.com,curve25519-sha256,curve25519-sha256@libssh.org
Ciphers chacha20-poly1305@openssh.com,aes256-gcm@openssh.com,aes128-gcm@openssh.com,aes256-ctr,aes128-ctr
MACs hmac-sha2-512-etm@openssh.com,hmac-sha2-256-etm@openssh.com,umac-128-etm@openssh.com
HostKeyAlgorithms ssh-ed25519,ssh-ed25519-cert-v01@openssh.com,rsa-sha2-512,rsa-sha2-256
PubkeyAcceptedAlgorithms ssh-ed25519,ssh-ed25519-cert-v01@openssh.com,sk-ssh-ed25519@openssh.com,rsa-sha2-512,rsa-sha2-256
HostKey /etc/ssh/ssh_host_ed25519_key
HostKey /etc/ssh/ssh_host_rsa_key
```

- `mlkem768x25519-sha256` (available by default since OpenSSH 9.9) and `sntrup761x25519-sha512`
  protect against harvest-now-decrypt-later; both lead the current sshd default KexAlgorithms list.
  `WarnWeakCrypto` (the `no-pq-kex` flag) controls warnings about connections without a post-quantum KEX.
- Remove `diffie-hellman-group1-sha1`, `group14-sha1`, `ecdh-sha2-*` if policy
  permits (FIPS environments may need `ecdh-sha2-nistp256` and AES-GCM only).
- Check the effective config with `sshd -T` and look at the kexalgorithms, ciphers, macs and hostkeyalgorithms lines.
- The first obtained value of a keyword is used in sshd_config, so a distro default earlier in the file overrides yours.

## Terrapin (CVE-2023-48795)

Prefix truncation attack on connections using ChaCha20-Poly1305 or a CBC cipher with
Encrypt-then-MAC. The "strict key exchange" countermeasure takes effect only if both client and server support it.
If either cannot be updated, remove `chacha20-poly1305@openssh.com` and CBC+ETM combinations.

## Audit

```bash
ssh-audit host.example.com          # lists algorithms and flags weak/legacy ones
ssh -Q kex; ssh -Q cipher           # what the local client supports
```

Test from your oldest required client before reloading; keep a session open while reloading.

## Verify

- [ ] `ssh-audit` shows no failures; a PQ KEX is negotiated (check with `ssh -v`).
- [ ] `sshd -T` reflects the intended lists (no earlier override).
- [ ] Oldest supported client connects successfully.

## Checked
2026-11-01. Confirmed against the sshd_config man page (KexAlgorithms list and default, first-obtained-value rule, WarnWeakCrypto no-pq-kex), OpenSSH 9.9 release notes (mlkem768x25519-sha256 available by default) and terrapin-attack.com (ChaCha20-Poly1305 or CBC+EtM affected; strict KEX needs both sides). Removed: default-since/10.0/10.1 version claims, strict-KEX 9.6 version, moduli awk command, nmap line, grep pipeline, ssh -v output text.
Method: documentation only; no commands were run.
