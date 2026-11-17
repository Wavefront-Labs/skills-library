---
id: computing-software.cybersecurity-defensive.system-hardening.sshd-hardening
name: sshd-hardening
category: computing-software
field: cybersecurity-defensive
product: system-hardening
tags: [linux-hardening, sshd-hardening, openssh, sshd-config, key-based-auth, ssh-ciphers, fail2ban]
level: practitioner
status: docs-checked
description: "Harden OpenSSH servers: key-only auth, no root login, modern KEX and ciphers, AllowGroups, drop-in configs, sshd -T verification and safe rollout without lockout."
sources: ["https://github.com/openssh/openssh-portable/blob/master/sshd_config.5", "https://github.com/openssh/openssh-portable/blob/master/sshd.8"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# sshd hardening

**Goal:** SSH accepts only key (or certificate) logins from permitted groups, with modern crypto, and you can prove it.

## Config (drop-in `/etc/ssh/sshd_config.d/10-hardening.conf`)
```
PermitRootLogin no
PasswordAuthentication no
KbdInteractiveAuthentication no
PubkeyAuthentication yes
AuthenticationMethods publickey
PermitEmptyPasswords no
AllowGroups ssh-users
MaxAuthTries 3
LoginGraceTime 30
ClientAliveInterval 300
ClientAliveCountMax 2
X11Forwarding no
AllowAgentForwarding no
AllowTcpForwarding no
PermitUserEnvironment no
LogLevel VERBOSE
KexAlgorithms sntrup761x25519-sha512@openssh.com,curve25519-sha256,curve25519-sha256@libssh.org   # also mlkem768x25519-sha256 on releases that list it
Ciphers chacha20-poly1305@openssh.com,aes256-gcm@openssh.com,aes128-gcm@openssh.com
MACs hmac-sha2-512-etm@openssh.com,hmac-sha2-256-etm@openssh.com
```
- For each keyword sshd uses the **first value obtained** (sshd_config(5)). `Include` is processed where it appears (globs expand in lexical order), so keep `Include /etc/ssh/sshd_config.d/*.conf` at the top of the main file and make sure nothing earlier sets these keywords.
- Only list algorithms your build supports: `ssh -Q KexAlgorithms`, `ssh -Q cipher` and `ssh -Q mac` print the supported lists; the defaults are in sshd_config(5).
- `/etc/moduli` holds the Diffie-Hellman group parameters sshd uses (moduli(5)).
- Consider SSH certificates (`TrustedUserCAKeys`) instead of scattered `authorized_keys`.

## Safe rollout
1. `sshd -t` to syntax-check.
2. `sshd -T | grep -Ei 'permitrootlogin|passwordauth|ciphers|kexalg'` shows the **effective** values.
3. Keep the current session open; reload the SSH daemon with your init system; test a new login in a second terminal before closing.
4. For `Match` blocks: `sshd -T -C user=alice,host=x,addr=10.0.0.5`.

## Brute force
Key-only auth makes password spraying moot; still limit unauthenticated connections to reduce log noise (`MaxStartups start:rate:full`, for example `10:30:60`, and `PerSourceMaxStartups`).

## Verify
- [ ] `ssh -o PubkeyAuthentication=no user@host` fails with "Permission denied (publickey)".
- [ ] `sshd -T` lists only the intended `kexalgorithms`, `ciphers` and `macs`.
- [ ] Root login denied.

## Checked
Checked 2026-10-25 against sshd_config(5) and sshd(8) in the openssh-portable repository (current master). Confirmed: first-obtained-value rule, `Include` semantics, every keyword in the sample (PermitRootLogin, PasswordAuthentication, KbdInteractiveAuthentication, PubkeyAuthentication, AuthenticationMethods, PermitEmptyPasswords, AllowGroups, MaxAuthTries, LoginGraceTime, ClientAliveInterval/CountMax, X11Forwarding, AllowAgentForwarding, AllowTcpForwarding, PermitUserEnvironment, LogLevel, KexAlgorithms, Ciphers, MACs), the algorithm names (including `sntrup761x25519-sha512@openssh.com`, `mlkem768x25519-sha256`, `chacha20-poly1305@openssh.com`, `aes256-gcm@openssh.com`, `hmac-sha2-512-etm@openssh.com`), `MaxStartups` `start:rate:full`, `sshd -T` and `-T -C user=,host=,addr=`, and `ssh -Q`. Removed unconfirmed: the moduli filtering one-liner, RHEL crypto-policy note, fail2ban and ssh-audit, and the CIS and Mozilla guideline references (not read).

Method: documentation only; no commands were run.
