---
id: computing-software.devops-ci-cd.argocd-image-updater.git-commit-signing-and-api-method
name: git-commit-signing-and-api-method
category: computing-software
field: devops-ci-cd
product: argocd-image-updater
tags: [argocd-image-updater, commit-signing, gpg, ssh-signing, sign-off, git-commit-method, verified-commits, github-app]
level: sme
status: docs-checked
description: "Sign write-back commits with a GPG or SSH key, enable sign-off, or create commits through the GitHub API with git-commit-method=api so GitHub marks them Verified."
sources: ["https://github.com/argoproj-labs/argocd-image-updater/blob/master/docs/basics/update-methods.md", "https://github.com/argoproj-labs/argocd-image-updater/blob/master/docs/install/cmd/run.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Commit signing and API commits

Two reasons to sign: SCM branch protection that requires signed commits, or Argo CD source verification policies.

Branch protection needs a bot user account with the GPG or SSH key attached to it, username and email matching that account, and HTTPS or SSH access with a user account. GitHub App access cannot be verified through the git command line.

Source verification does not need the key tied to an SCM user.

SSH signing (ConfigMap `argocd-image-updater-config`; the private key must be mounted in the pod):

```yaml
data:
  git.commit-sign-off: "true"
  git.commit-signing-key: /app/ssh-keys/id_rsa
  git.commit-signing-method: "ssh"
```

GPG signing: install the private key in the pod, keep the default `git.commit-signing-method` of `openpgp` and set `git.commit-signing-key` to the key ID, for example `3AA5C34371567BD2`. Flags: `--git-commit-signing-key`, `--git-commit-signing-method`, `--git-commit-sign-off`.

API commits: `GIT_COMMIT_METHOD=api` (or `--git-commit-method api`) creates commits through the GitHub GraphQL API as the GitHub App bot, signed by GitHub and shown as Verified, for both direct push and PR flows. Notes:

- GitHub App credentials are required; otherwise it falls back to git with a warning
- user, email and signing settings are ignored
- GraphQL rate limits apply; if exhausted, writes fail and retry next cycle, so raise `--interval` or spread apps across installations

## Checked

2026-11-04. Confirmed against update-methods.md (Enabling commit signature signing, SSH and GPG ConfigMap keys, Signed commits via the GitHub API with its notes) and the run command page (--git-commit-method, --git-commit-signing-key, --git-commit-signing-method defaulting to openpgp, --git-commit-sign-off).

Method: documentation only; no commands were run.
