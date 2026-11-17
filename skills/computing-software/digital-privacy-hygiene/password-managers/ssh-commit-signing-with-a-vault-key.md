---
id: computing-software.digital-privacy-hygiene.password-managers.ssh-commit-signing-with-a-vault-key
name: ssh-commit-signing-with-a-vault-key
category: computing-software
field: digital-privacy-hygiene
product: password-managers
tags: [digital-privacy-hygiene, password-managers, ssh-commit-signing, ssh-agent-password-manager, git]
level: practitioner
status: draft
description: "Sign git commits with an SSH key held in 1Password or Bitwarden's SSH agent, configure allowed signers, and get Verified badges on GitHub."
sources:
  - "https://developer.1password.com/docs/ssh/git-commit-signing/"
  - "https://bitwarden.com/help/ssh-agent/"
  - "https://docs.github.com/en/authentication/managing-commit-signature-verification/about-commit-signature-verification"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# SSH commit signing with a vault-held key

**Goal:** commits are signed with a key that never sits unencrypted on disk, and each signature needs your
approval (biometric/unlock prompt).

## Prerequisites
- SSH key item in the vault with the agent enabled (1Password SSH agent, or Bitwarden desktop SSH agent).
- `SSH_AUTH_SOCK` pointing at the manager's agent socket (1Password: configured via its `~/.ssh/config`
  IdentityAgent snippet; Bitwarden: `~/.bitwarden-ssh-agent.sock`).

## Git config
```
git config --global gpg.format ssh
git config --global user.signingkey "key::ssh-ed25519 AAAA...your-public-key"
git config --global commit.gpgsign true
git config --global tag.gpgsign true
```
1Password alternatively sets `gpg.ssh.program` to its `op-ssh-sign` helper (macOS path inside the 1Password
app bundle; Windows `op-ssh-sign.exe` in the 1Password install folder). Its "Configure Commit Signing" button
writes this for you.

## Verification locally
```
echo "you@example.com $(cat id_signing.pub)" >> ~/.config/git/allowed_signers
git config --global gpg.ssh.allowedSignersFile ~/.config/git/allowed_signers
git log --show-signature -1
```

## GitHub/GitLab
Add the same public key as a **Signing key** (GitHub: Settings > SSH and GPG keys > New SSH key > Key type:
Signing Key). Separate from the authentication key entry even if it's the same key.

## Gotchas
- WSL/devcontainers need the agent socket forwarded, or signing fails with "agent refused operation".
- The commit email must match a verified email on the account for the Verified badge.
