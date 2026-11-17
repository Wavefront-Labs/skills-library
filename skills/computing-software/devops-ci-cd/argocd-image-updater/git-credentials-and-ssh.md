---
id: computing-software.devops-ci-cd.argocd-image-updater.git-credentials-and-ssh
name: git-credentials-and-ssh
category: computing-software
field: devops-ci-cd
product: argocd-image-updater
tags: [argocd-image-updater, git-credentials, repocreds, git-secret, ssh-private-key, insecure, known-hosts]
level: practitioner
status: docs-checked
description: "Give git write-back its own credentials with git:secret:name: HTTPS username and password, or an SSH private key, including the insecure field defaults and namespace rule."
sources: ["https://github.com/argoproj-labs/argocd-image-updater/blob/master/docs/basics/update-methods.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Git credentials: HTTPS and SSH

`writeBackConfig.method` takes `git:<credref>`:

- `repocreds` (default): reuse repository credentials from Argo CD settings
- `secret:<secret>`: secret in the CR's namespace
- `secret:<namespace>/<secret>`: the namespace must equal the CR's namespace; cross-namespace references are rejected

```yaml
spec:
  writeBackConfig:
    method: "git:secret:git-creds"
```

HTTPS user credentials need keys `username` and `password` (password or PAT with write access):

```bash
kubectl -n argocd-image-updater create secret generic git-creds \
  --from-literal=username=someuser \
  --from-literal=password=somepassword
```

SSH needs the key `sshPrivateKey` (OpenSSH PEM): `--from-file=sshPrivateKey=~/.ssh/id_rsa`.

TLS and host keys: the optional `insecure` secret field defaults to `"true"` for username/password and SSH secrets, so certificate (HTTPS) and host key (SSH) checks are skipped; SSH logs a warning on every push. Add `insecure=false` to verify. With SSH verification on, host keys come from the `argocd-ssh-known-hosts-cm` ConfigMap mounted at `/app/config/ssh`, and the Git host must be listed or the push fails. An invalid `insecure` value keeps the default and logs a warning.

## Checked

2026-11-04. Confirmed against update-methods.md (Specifying Git credentials: credref values, same-namespace rule, username/password and sshPrivateKey secrets, insecure defaults, argocd-ssh-known-hosts-cm mounted at /app/config/ssh).

Method: documentation only; no commands were run.
