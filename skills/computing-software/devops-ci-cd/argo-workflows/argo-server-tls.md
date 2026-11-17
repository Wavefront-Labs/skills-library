---
id: computing-software.devops-ci-cd.argo-workflows.argo-server-tls
name: argo-server-tls
category: computing-software
field: devops-ci-cd
product: argo-workflows
tags: [argo-server-tls, argo-secure, insecure-skip-verify, tls-min-version, readiness-probe]
level: practitioner
status: docs-checked
description: "Choose plain, encrypted or encrypted-and-verified Argo Server TLS, matching CLI flags and variables, and the TLS_MIN_VERSION values."
sources: ["https://argo-workflows.readthedocs.io/en/latest/tls/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Argo Server transport security
Three options, and you should also enable an auth mode.

1. Default: the image defaults to Encrypted with a self-signed certificate expiring after 365 days.
2. Plain text (development): `argo server --secure=false` or `ARGO_SECURE=false`. Front it with an HTTPS proxy to secure the UI.
3. Encrypted (dev and test): `argo server --secure`. Run the CLI with `--secure --insecure-skip-verify` (`ARGO_SECURE=true`, `ARGO_INSECURE_SKIP_VERIFY=true`). Update the `argo-server` readiness probe to `httpGet: {scheme: HTTPS}`.
4. Encrypted and verified (production): run your own HTTPS proxy with real certificates in front of `argo server --secure`, and the CLI needs only `--secure` / `ARGO_SECURE=true`.

Minimum TLS version: set `TLS_MIN_VERSION` to an int; default v1.2. Values: v1.0 is 769, v1.1 is 770, v1.2 is 771, v1.3 is 772.

Mutual TLS: pass `--client-certificate` and `--client-key` together, and `--certificate-authority` to trust the signing CA. These flags have no `ARGO_*` environment variable equivalents, and kubeconfig client certificates are not used automatically in server mode.

## Checked
2026-11-03. Confirmed against the Argo Workflows Transport Layer Security page: the default 365-day self-signed certificate, plain, encrypted and verified options, CLI flags and variables, readiness probe scheme, TLS_MIN_VERSION values, and the mutual TLS flags (added from the page). Removed uncited advice on skipping verification.
Method: documentation only; no commands were run.
