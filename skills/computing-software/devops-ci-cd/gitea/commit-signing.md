---
id: computing-software.devops-ci-cd.gitea.commit-signing
name: commit-signing
category: computing-software
field: devops-ci-cd
product: gitea
tags: [gitea-signing-key, gitea, repository-signing, signing-format-ssh, trusted-ssh-keys, merges-basesigned, signing-key-gpg]
level: advanced
status: docs-checked
description: "Make Gitea sign its own commits (GPG or SSH key) and verify signatures: [repository.signing] SIGNING_KEY, INITIAL_COMMIT, CRUD_ACTIONS, WIKI, MERGES, TRUSTED_SSH_KEYS."
sources: ["https://docs.gitea.com/administration/signing/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Gitea commit signing

Gitea verifies GPG/SSH signatures against keys in its database (or the default Git key) and SSH signatures against `TRUSTED_SSH_KEYS`. It does not check expiry or revocation and does not use keyservers. A grey unlocked icon means no key found; a red unlocked icon means signed with a key id Gitea cannot match. The signer need not be author or committer.

Gitea itself creates commits on repo init, wiki changes, web-editor and API CRUD actions, and PR merges, using the server's `git`, so server `gpg` (or `ssh-keygen` for SSH) does the signing. For GPG, prefer installing only a signing subkey.

## SSH key
`ssh-keygen -t ed25519 -f gitea-signing-key` (no password), keep it beside the config.
```ini
[repository.signing]
SIGNING_KEY = /path/to/gitea-signing-key.pub
SIGNING_NAME = Gitea
SIGNING_EMAIL = gitea@example.com
SIGNING_FORMAT = ssh
INITIAL_COMMIT = always
CRUD_ACTIONS = pubkey, twofa, parentsigned
WIKI = never
MERGES = pubkey, twofa, basesigned, commitssigned
```
`SIGNING_FORMAT = ssh` replaces the default `openpgp`; `SIGNING_NAME` and `SIGNING_EMAIL` are required for verification. `TRUSTED_SSH_KEYS = ssh-<algo> <key1>, ssh-<algo> <key2>` keeps old keys verifiable after rotation. `default` and per-repo keys are not supported for SSH.

## SIGNING_KEY values
`none` (never sign), `default` (use `commit.gpgsign`, `user.signingkey`, `user.name`, `user.email` from git config), a GPG `KEYID` (also set name and email), or a `.pub` path for SSH.
Since 1.17 Gitea runs git with its own home `[git].HOME_PATH` (default `%(APP_DATA_PATH)/home`) and config `{HOME_PATH}/.gitconfig`; put custom git config in `/etc/gitconfig` or there, and `.gnupg` under that home, or set `$GNUPGHOME`.

## Policy keys
Options other than `never`/`always` combine as a comma list, all must hold.
- `INITIAL_COMMIT`: never, pubkey, twofa, always.
- `WIKI` and `CRUD_ACTIONS`: never, pubkey, twofa, parentsigned, always.
- `MERGES`: never, pubkey, twofa, basesigned, headsigned, commitssigned, approved, always.

## Public keys over the API
`/api/v1/signing-key.gpg`, per-repo `/api/v1/repos/:username/:reponame/signing-key.gpg`, and `/api/v1/signing-key.pub` for the SSH key.

## Checked

2026-11-03: read https://docs.gitea.com/administration/signing/ line by line; the commands, options, defaults and values stated above match those pages.
Removed: nothing; every claim was confirmed.
Method: documentation only; no commands were run.
