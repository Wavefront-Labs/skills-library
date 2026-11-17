---
id: computing-software.devops-ci-cd.argo-workflows.argo-server-auth-mode
name: argo-server-auth-mode
category: computing-software
field: devops-ci-cd
product: argo-workflows
tags: [auth-mode, argo-server-auth, client-auth, sso-auth, token-review-cache]
level: practitioner
status: docs-checked
description: "Pick the Argo Server --auth-mode values server, client and sso, including the SelfSubjectReview requirement of client mode and its token review cache."
sources: ["https://argo-workflows.readthedocs.io/en/latest/argo-server-auth-mode/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Argo Server auth modes
Set how the Argo Server authenticates to Kubernetes with one or more `--auth-mode` flags:

```bash
argo server --auth-mode=sso --auth-mode=client
```

Modes:
- `server`: in hosted mode use the server's service account; in local mode use your kubeconfig.
- `client`: use the Kubernetes bearer token supplied by the client (an access token). The server validates it with a `SelfSubjectReview` before serving the request, so this needs Kubernetes 1.28 or later. Successful reviews are cached for `ARGO_SERVER_TOKEN_REVIEW_CACHE_TTL`, default `1m`, to reduce API server load.
- `sso`: single sign-on. It uses the same service account as `server` for RBAC unless SSO RBAC is enabled.

The default is `client`.

Use one or several `--auth-mode` flags.

## Checked
2026-11-03. Confirmed against the Argo Workflows Argo Server Auth Mode page: the three modes, the SelfSubjectReview and Kubernetes 1.28 requirement, the `ARGO_SERVER_TOKEN_REVIEW_CACHE_TTL` default of 1m, the default of `client` and the example flags. Removed unsupported advice about scoping the server account and combining modes, and the uncited hosted/local explanation.
Method: documentation only; no commands were run.
