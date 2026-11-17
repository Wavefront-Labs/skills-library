---
id: computing-software.devops-ci-cd.forgejo.instance-commit-signing-keys
name: instance-commit-signing-keys
category: computing-software
field: devops-ci-cd
product: forgejo
tags: [commit-signing, signing-key, ssh-signing, gpg-signing]
level: advanced
status: docs-checked
description: "Configure Forgejo to sign commits it creates itself using an SSH or GPG instance key."
sources:
  - https://forgejo.org/docs/latest/admin/advanced/signing/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Forgejo can sign commits it generates itself: repository initialisation, wiki changes, web editor or API file changes, and pull request merges. Settings live in `[repository.signing]`.

SSH is strongly preferred when its requirements are met: Git 2.34.0 or newer and `ssh-keygen` 8.2p1 or newer. Create a dedicated OpenSSH key pair for the instance, then set `FORMAT = ssh` and `SIGNING_KEY = /absolute/path/to/key.pub`, an absolute path to the public key with the private key at the same path without `.pub`. Also set the committer identity with `SIGNING_NAME` and `SIGNING_EMAIL`. The key can also be held in a TPM via ssh-tpm-agent, which needs SSH_AUTH_SOCK set for the Forgejo process.

GPG has two modes. `SIGNING_KEY = default` uses git config: if `commit.gpgsign` is true it takes `user.signingkey`, `user.name` and `user.email`. Or give a GPG key ID plus `SIGNING_NAME` and `SIGNING_EMAIL`; Forgejo looks in `GNUPGHOME`, else `[git].HOME_PATH/.gnupg`. Take care that GPG does not use that keyring by default.

Public keys are published at `/api/v1/signing-key.gpg` or `/api/v1/signing-key.ssh`, and per repository at `/api/v1/repos/{username}/{reponame}/signing-key.gpg`.

## Checked

2026-11-04. Confirmed against the Forgejo Instance Commit Signing page: the signed operations, SSH requirements and settings, GPG default and key-ID modes, keyring location, ssh-tpm-agent with SSH_AUTH_SOCK, and the three API routes. Nothing removed.

Method: documentation only; no commands were run.
