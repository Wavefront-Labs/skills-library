---
id: computing-software.devops-ci-cd.argocd-image-updater.git-github-app-credentials
name: git-github-app-credentials
category: computing-software
field: devops-ci-cd
product: argocd-image-updater
tags: [argocd-image-updater, github-app, git-credentials, github-enterprise, mtls, git-secret, proxy]
level: advanced
status: docs-checked
description: "Use GitHub App credentials for git write-back: required secret keys, optional enterprise base URL, mTLS and proxy fields, and the insecure default that changed to false."
sources: ["https://github.com/argoproj-labs/argocd-image-updater/blob/master/docs/basics/update-methods.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# GitHub App credentials for write-back

When the repository is accessed over HTTPS, the Git secret can hold GitHub App credentials instead of a user password. Required keys:

- `githubAppID`
- `githubAppInstallationID` (the organisation installation ID)
- `githubAppPrivateKey`

The app must be installed on the target repository with write access.

```bash
kubectl -n argocd-image-updater create secret generic git-creds \
  --from-literal=githubAppID=applicationid \
  --from-literal=githubAppInstallationID=installationid \
  --from-literal=githubAppPrivateKey='-----BEGIN RSA PRIVATE KEY-----PRIVATEKEYDATA-----END RSA PRIVATE KEY-----'
```

Optional keys:

| Key | Meaning | Default |
|---|---|---|
| `githubAppEnterpriseBaseUrl` | e.g. `https://github.example.com/api/v3` | github.com |
| `tlsClientCertData` / `tlsClientCertKey` | PEM client cert and key for mTLS | empty |
| `insecure` | `"true"` or `"false"` | `"false"` |
| `proxy` | HTTP(S) proxy URL | empty |

Behaviour change: secret-based GitHub App credentials used to skip TLS verification always; they now default to `insecure: "false"`, matching repository credentials from Argo CD settings. If a GitHub Enterprise instance uses a self-signed or internal CA, either set `insecure: "true"` in the secret or install the CA in the container trust store. An invalid `insecure` value falls back to `"false"` without a warning.

Reference it with `method: "git:secret:git-creds"`.

## Checked

2026-11-04. Confirmed against update-methods.md (GitHub App secret fields, optional-fields table with defaults, Enterprise example, insecure behaviour change and the self-signed CA options, invalid-value fallback).

Method: documentation only; no commands were run.
