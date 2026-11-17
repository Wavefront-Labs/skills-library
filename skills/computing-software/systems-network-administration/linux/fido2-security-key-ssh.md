---
id: computing-software.systems-network-administration.linux.fido2-security-key-ssh
name: fido2-security-key-ssh
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, ssh-keys, ed25519-sk, fido2-ssh, security-key, resident-keys, verify-required, ssh-keygen]
level: practitioner
status: docs-checked
description: "Use FIDO2 hardware keys for SSH: ed25519-sk/ecdsa-sk key generation, resident vs non-resident keys, touch and PIN (verify-required), server requirements and backup keys."
sources:
  - https://github.com/openssh/openssh-portable/blob/master/ssh-keygen.1
  - https://github.com/openssh/openssh-portable/blob/master/sshd.8
  - https://github.com/openssh/openssh-portable/blob/master/sshd_config.5
  - https://github.com/openssh/openssh-portable/blob/master/ssh_config.5
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# FIDO2 security-key SSH keys

The private key stays on the token; by default every authentication needs a touch (and optionally PIN). Client and server must be built with FIDO key support; `SecurityKeyProvider` (or `ssh-keygen -w`) selects the middleware library.

## Generate
```bash
ssh-keygen -t ed25519-sk -C "alice yubikey-1"                          # file stub ~/.ssh/id_ed25519_sk (handle, not the key)
ssh-keygen -t ed25519-sk -O resident -O application=ssh:work -O verify-required
ssh-keygen -t ecdsa-sk                                                  # for tokens without ed25519 support
```
- **Non-resident** (default): the stub file + the token are both needed; stub can be copied to other machines.
- **Resident** (`-O resident`): stored on the token; on a new machine `ssh-keygen -K` downloads stubs (needs PIN).
- `-O verify-required`: PIN/biometric on every use (server can demand it: `PubkeyAuthOptions verify-required`).
- `-O no-touch-required` exists but defeats the point (server must allow it per key).

## Deploy
`ssh-copy-id -i ~/.ssh/id_ed25519_sk.pub host` → line starts with `sk-ssh-ed25519@openssh.com`.
Server: `PubkeyAcceptedAlgorithms` must include `sk-ssh-ed25519@openssh.com` (the default list does).

## Operations
- Register **two** tokens (primary + backup in a safe) on every account.
- Automation/CI can't touch — use separate service keys or certificates.

## Troubleshooting
Run `ssh -v` to see whether the key was offered and signed; if enrollment of `ed25519-sk` fails, try `ecdsa-sk`, which is the alternative sk key type.

## Verify
- [ ] Login succeeds only after the token is touched (and PIN entered if `verify-required`); backup token also works.

## Checked
Checked 2026-10-25 against OpenSSH portable master manual sources (ssh.1, ssh_config.5, sshd.8, sshd_config.5, ssh-keygen.1, ssh-add.1, scp.1, sftp.1).
Confirmed: `-t ed25519-sk` and `ecdsa-sk`, `-O resident`, `-O application=ssh:...`, `-O verify-required`, `-O no-touch-required` (with the matching authorized_keys option), `ssh-keygen -K`, `PubkeyAuthOptions` accepting touch-required and verify-required, the default PubkeyAcceptedAlgorithms including `sk-ssh-ed25519@openssh.com`, and `SecurityKeyProvider`.
Removed as unconfirmed: OpenSSH 8.2 version gate, libfido2 and udev troubleshooting, agent support statement, and exact error messages.

Method: documentation only; no commands were run.
