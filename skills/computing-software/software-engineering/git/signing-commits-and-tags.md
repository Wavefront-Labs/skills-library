---
id: computing-software.software-engineering.git.signing-commits-and-tags
name: signing-commits-and-tags
category: computing-software
field: software-engineering
product: git
tags: [git, git-repository-tools, commit-signing, ssh-signing, gpg-signing, verified-commits, allowed-signers, supply-chain]
level: practitioner
status: verified
description: "Sign commits and tags with SSH or GPG keys, configure allowed signers for verification, and get forge 'Verified' badges and signed-commit rules working."
sources:
  - https://git-scm.com/book/en/v2/Git-Tools-Signing-Your-Work
  - https://git-scm.com/docs/git-config
  - https://git-scm.com/docs/pretty-formats
  - https://git-scm.com/docs/git-verify-commit
  - https://docs.github.com/en/authentication/managing-commit-signature-verification/about-commit-signature-verification
  - https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Signing commits and tags

**Goal:** prove commits and release tags came from you, and enforce it where required.

## 1. SSH signing (simplest; Git 2.34+)
```bash
git config --global gpg.format ssh
git config --global user.signingkey ~/.ssh/id_ed25519.pub
git config --global commit.gpgsign true
git config --global tag.gpgsign true
```
`user.signingkey` can be a path to the private or public SSH key (public key when an agent is used) or a literal public key prefixed with `key::`. Register the public key with your forge so it can verify the signatures. OpenSSH 8.7's `ssh-keygen` has broken SSH-signing support; the Git 2.34 release notes say to avoid it and use OpenSSH 8.8 or later.

Local verification needs an allowed-signers file:
```bash
echo "me@example.com $(cat ~/.ssh/id_ed25519.pub)" >> ~/.config/git/allowed_signers
git config --global gpg.ssh.allowedSignersFile ~/.config/git/allowed_signers
git log --show-signature -1
```

## 2. GPG signing
```bash
gpg --full-generate-key
gpg --list-secret-keys --keyid-format=long    # copy the key id
git config --global user.signingkey 3AA5C34371567BD2
git config --global commit.gpgsign true
gpg --armor --export 3AA5C34371567BD2         # paste into the forge
```

## 3. Sign and verify
```bash
git commit -S -m "..."           # explicit, if not signing by default
git tag -s v2.0.0 -m "Release 2.0.0"
git verify-commit HEAD
git verify-tag v2.0.0
git log --format='%h %G? %GS %s'   # G good, B bad, U good/unknown validity, X expired signature, Y expired key, R revoked key, E cannot check, N none
```

## 4. Enforcement
- GitHub rulesets have a "Require signed commits" rule; see the GitHub docs for how it applies to merges made on the forge.
- Server-side: a `pre-receive` hook can run `git verify-commit` over the pushed range.
- With `gpg.format ssh`, a signature is trusted (`fully`) only when its key is in `gpg.ssh.allowedSignersFile`; otherwise verification fails in `git verify-commit` / `git verify-tag`. A repository that only allows signed commits can keep that file in the repository (path relative to the top level).

## Gotchas
- GitHub marks a commit or tag "Unverified" when its signature cannot be verified.
- Rebase re-creates commits; with `commit.gpgSign` set, Git's manual warns that operations such as rebase can result in a large number of commits being signed, and they are signed by you.
- With `gpg.format ssh` and an agent, set `user.signingkey` to the public key so Git asks the agent to sign.

## Verify
- `git verify-commit HEAD` exits 0 locally and the forge shows "Verified" on a pushed test commit.

## Checked

Checked 2026-10-25 against the git/git Documentation tree at master (latest commit 2026-10-22), the Git 2.34 release notes and the github/docs repository. Confirmed: `gpg.format` values (`openpgp`, `x509`, `ssh`), `gpg.ssh.allowedSignersFile` semantics and trust level, `user.signingKey` forms for ssh, `commit.gpgSign` and `tag.gpgSign`, `log.showSignature`, the full `%G?` status letter list and `%GS`; SSH signing introduced in Git 2.34 with the OpenSSH 8.7 caveat; GitHub marks unverifiable signatures "Unverified" and has a "Require signed commits" ruleset rule. Removed as unconfirmed: the Sigstore `gitsign` line, hardware-key touch behaviour, the pinentry-mac and `GPG_TTY` remarks, the forge-signs-squash-merges claim, the email-matching claim and the key-algorithm comment.

Run 2026-11-01 with Git for Windows, GnuPG 2.4.5 and OpenSSH 9.9p1 in throwaway repositories, with repository-local config instead of `--global`: GPG signing (`user.signingkey` with a `!` subkey, `commit.gpgsign`, `tag.gpgsign`, `git commit -S`, `git tag -s`, `git verify-commit` exit 0 for signed and 1 for unsigned, `git verify-tag`, `git log --show-signature`), `%G?` letters seen G (good), U (good signature, key validity unknown) and N (none), `%GS`; SSH signing (`gpg.format ssh`, `user.signingkey` as a public key path, `gpg.ssh.allowedSignersFile`: without the file `%G?` was N and git printed the allowedSignersFile error, with it G and `git verify-commit` and `git verify-tag` printed `Good "git" signature`). Not run: `gpg --full-generate-key` (interactive), `key::` literal keys, agent-based signing, forge Verified badges, rulesets, pre-receive hooks, the other `%G?` letters, rebase signing; these stay as documented.

Method: documentation plus commands run (GnuPG 2.4.5).
