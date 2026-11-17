---
id: computing-software.devops-ci-cd.flux.gitrepository-authentication
name: gitrepository-authentication
category: computing-software
field: devops-ci-cd
product: flux
tags: [gitrepository, authentication, ssh, basic-auth, bearer-token]
level: sme
status: docs-checked
description: "Authenticate a GitRepository over HTTPS basic or bearer token, SSH keys, or cloud providers, and the URL format pitfalls."
sources:
  - https://fluxcd.io/flux/components/source/gitrepositories/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`.spec.url` is an HTTP/S or SSH address. The scp-like form (`user@example.com:repository.git`) is not supported; use `ssh://user@example.com:22/repository.git`.

`.spec.secretRef.name` points to a Secret in the same namespace whose fields depend on the protocol.

HTTPS basic auth needs `username` and `password`. Bearer token auth needs `bearerToken`:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: basic-access-auth
type: Opaque
stringData:
  username: git-user
  password: <token>
```

SSH needs `identity` (private key) and `known_hosts` (host keys). A password-protected key also needs `password`. The CLI builds it and fills known_hosts:

```sh
flux create secret git podinfo-auth \
  --url=ssh://git@github.com/stefanprodan/podinfo \
  --private-key-file=./identity
```

`.spec.provider` selects OIDC-based auth instead of a Secret: `generic` (default, uses `secretRef`), `aws`, `azure` or `github`. The `aws` provider authenticates to CodeCommit with IAM credentials from the controller runtime identity, and `.spec.url` must be the CodeCommit HTTPS endpoint `https://git-codecommit.<region>.amazonaws.com/v1/repos/<name>`.

Related fields: `.spec.timeout` (default `60s`) bounds clone and other Git operations; `.spec.interval` is required. For proxies use `.spec.proxySecretRef`.

Debug auth failures with `kubectl describe gitrepository NAME` and `flux get sources git`.

## Checked

2026-11-03. Read the GitRepository reference (fluxcd.io/flux/components/source/gitrepositories/): URL formats and the scp-like warning, basic and bearer token Secrets, SSH `identity`/`known_hosts`/`password`, `provider` values, the CodeCommit URL format, `timeout` default 60s and `proxySecretRef`; `flux get sources git` checked on its CLI page. Nothing removed.

Method: documentation only; no commands were run.
