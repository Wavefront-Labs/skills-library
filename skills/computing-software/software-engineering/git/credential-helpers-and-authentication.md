---
id: computing-software.software-engineering.git.credential-helpers-and-authentication
name: credential-helpers-and-authentication
category: computing-software
field: software-engineering
product: git
tags: [git, git-repository-tools, credential-helper, git-credentials, https-auth, ssh-auth, personal-access-token, git-credential-manager]
level: practitioner
status: gated
description: "Authenticate Git over HTTPS and SSH: credential helpers per OS, tokens instead of passwords, per-host config, and debugging prompts and 403s."
sources:
  - https://git-scm.com/book/en/v2/Git-Tools-Credential-Storage
  - https://git-scm.com/docs/gitcredentials
  - https://github.com/git-ecosystem/git-credential-manager
  - https://docs.github.com/en/authentication/connecting-to-github-with-ssh
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Credential helpers and Git authentication

**Goal:** no password prompts, no plaintext tokens in URLs, and the right identity for each host.

## 1. HTTPS with a helper
```bash
git config --global credential.helper manager      # Git Credential Manager (Windows default; mac/Linux install)
git config --global credential.helper osxkeychain  # macOS keychain
git config --global credential.helper libsecret    # Linux desktop (build git-credential-libsecret)
git config --global credential.helper 'cache --timeout=3600'   # memory only
```
Avoid `store` except on throwaway machines: it writes `~/.git-credentials` in plaintext.
GitHub has removed password authentication for Git over HTTPS (docs.github.com, About remote repositories): use a PAT or a helper such as Git Credential Manager. Check other hosts' docs.

## 2. Per-host / per-org settings
```ini
[credential "https://github.com"]
    username = me
[credential "https://git.corp.example"]
    helper = !/usr/local/bin/corp-token-helper
[credential]
    useHttpPath = true    # different creds per repo path on the same host (e.g. Azure DevOps)
```

## 3. CI and scripts
```bash
git -c http.extraHeader="Authorization: Bearer $TOKEN" clone https://git.example.com/org/repo.git
# or a credential helper reading an env var (checked: `git credential fill` returns username=x-access-token and the $GH_TOKEN value):
git config credential.helper '!f() { echo username=x-access-token; echo "password=$GH_TOKEN"; }; f'
```
Never embed tokens in remote URLs (`https://token@host/...`): they land in `.git/config`, logs and process listings.

## 4. SSH
```bash
ssh-keygen -t ed25519 -C "me@example.com"
ssh -T git@github.com
```
Multiple accounts on one host via `~/.ssh/config`:
```
Host github-work
    HostName github.com
    IdentityFile ~/.ssh/id_work
    IdentitiesOnly yes
```
then `git remote set-url origin git@github-work:corp/repo.git`. Or `core.sshCommand` per repo / `includeIf`.

## Debugging
```bash
GIT_TRACE=1 GIT_CURL_VERBOSE=1 git fetch 2>&1 | grep -iE 'auth|credential|HTTP/'
GIT_SSH_COMMAND="ssh -v" git fetch
printf 'protocol=https\nhost=github.com\n\n' | git credential fill    # what the helper returns
printf 'protocol=https\nhost=github.com\n\n' | git credential reject  # drop a stale stored token
```
- 403 after rotating a token: the helper is returning the old one; `reject` it.
- 401/403 on SAML SSO orgs: a classic PAT must be authorised for the org after creation (GitHub docs, authorizing a PAT for SSO).

## Verify
- `git ls-remote origin` succeeds non-interactively, and `git config --show-origin --get-all credential.helper` lists only the helpers you expect.

> Review note: some commands in this skill (Git Credential Manager, exiftool/pandoc textconv, signed tags, the `e` hunk-edit recipe) were not run during review. (gated: unconfirmed, source is paywalled or blocked)
