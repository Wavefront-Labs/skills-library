---
id: computing-software.cryptography-implementation.protocol-implementation.signing-with-ssh-keygen-y
name: signing-with-ssh-keygen-y
category: computing-software
field: cryptography-implementation
product: protocol-implementation
tags: [cryptography-implementation, protocol-implementation, ssh, openssh, ssh-signing, ssh-keygen-y, allowed-signers, git-commit-signing, sshsig, namespace]
level: practitioner
status: docs-checked
description: "Sign and verify files and git commits with SSH keys (ssh-keygen -Y sign/verify): namespaces, allowed_signers format, git gpg.format=ssh setup, and revocation."
sources: ["https://man.openbsd.org/ssh-keygen#Y", "https://git-scm.com/docs/git-config#Documentation/git-config.txt-gpgformat"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Signing with ssh-keygen -Y

OpenSSH `ssh-keygen -Y` can create and check detached signatures with existing
SSH keys (SSHSIG format). It is a simple alternative to PGP for release files and git commits.

## Files

```bash
ssh-keygen -Y sign -f ~/.ssh/id_ed25519 -n file release.tar.gz      # -> release.tar.gz.sig
# allowed_signers: <principal> [options] <key-type> <key>
echo 'alice@example.com namespaces="file,git" ssh-ed25519 AAAAC3...' > allowed_signers
ssh-keygen -Y verify -f allowed_signers -I alice@example.com -n file \
  -s release.tar.gz.sig < release.tar.gz
ssh-keygen -Y find-principals -f allowed_signers -s release.tar.gz.sig   # who signed it
ssh-keygen -Y check-novalidate -n file -s release.tar.gz.sig < release.tar.gz  # sig valid, signer unknown
```

- The **namespace** (`-n`) is domain separation: a signature made for `git`
  does not verify as `file`. Use a specific one per use (`file`,
  `git`, `myapp-config@example.com`).
- `allowed_signers` options: `namespaces="..."`, `valid-after`, `valid-before`,
  `cert-authority` (trust any cert from an SSH CA for that principal pattern).
- Revocation: `-r revocation_file` on verify.

## Git

```bash
git config --global gpg.format ssh
git config --global user.signingkey <your SSH public key>
git config --global gpg.ssh.allowedSignersFile <path to allowed_signers>
```

Git then verifies signatures against `allowed_signers`; the file can carry
`valid-after` and `valid-before` so a signing key can change without invalidating older signatures.

## Limits

- No web of trust or key expiry beyond `valid-before` in allowed_signers;
  distribution of trusted keys is your job.
- Separate signing keys from login keys if your policy rotates them differently.

## Verify

- [ ] Verify succeeds with correct principal/namespace; fails with wrong namespace or modified file.
- [ ] Commit signatures are checked against an allowed_signers file you control.

## Checked

Date: 2026-11-01. Confirmed in the OpenBSD ssh-keygen manual (-Y sign, verify, find-principals, check-novalidate, -n namespace, -r revocation_file, allowed_signers options namespaces, valid-after, valid-before, cert-authority) and the git-config documentation (gpg.format, gpg.ssh.allowedSignersFile, valid-after/valid-before handling). Removed: the OpenSSH version number, hardware-key and agent claims, GitHub/GitLab Verified behaviour, `commit.gpgsign`, `git log --show-signature`, `git verify-commit` and the PROTOCOL.sshsig source link.
Method: documentation only; no commands were run.
