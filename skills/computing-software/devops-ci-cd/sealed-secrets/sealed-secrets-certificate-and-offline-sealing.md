---
id: computing-software.devops-ci-cd.sealed-secrets.sealed-secrets-certificate-and-offline-sealing
name: sealed-secrets-certificate-and-offline-sealing
category: computing-software
field: devops-ci-cd
product: sealed-secrets
tags: [sealed-secrets, kubeseal, fetch-cert, certificate, offline, sealed-secrets-cert, public-key]
level: practitioner
status: docs-checked
description: "Fetch and store the Sealed Secrets public certificate so kubeseal can seal offline, including URL certs, the SEALED_SECRETS_CERT variable and renewal."
sources: ["https://github.com/bitnami/sealed-secrets"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Sealed secrets certificate and offline sealing

The certificate (public key) is used for sealing and must be available wherever `kubeseal` runs. It is not secret, but you must make sure you use the right one.

By default `kubeseal` fetches the certificate from the controller at runtime, which needs secure access to the Kubernetes API server. That is convenient interactively but brittle on clusters with special configuration, for example private GKE clusters with firewalls between the control plane and nodes.

Offline workflow:

```bash
kubeseal --fetch-cert >mycert.pem
kubeseal --cert mycert.pem <mysecret.json >mysealedsecret.json
```

The certificate is also printed to the controller log on startup.

Since v0.9.x the sealing certificates are renewed automatically every 30 days, so teams should refresh their stored copy periodically. Since v0.9.2 `kubeseal --cert` also accepts a URL, letting internal automation publish the certificate somewhere trusted:

```bash
kubeseal --cert https://your.intranet.company.com/sealed-secrets/your-cluster.cert
```

The `SEALED_SECRETS_CERT` environment variable is also recognised (the README suggests direnv for per-project values). `--fetch-cert` returns the certificate of the most recent sealing key, ordered by the controller's key-order-priority setting.

The README says HSM and cloud KMS-backed key management is in progress; at the time of writing, keys live in Kubernetes Secrets.

## Checked
Date: 2026-11-04. Documentation: bitnami-labs/sealed-secrets README (raw markdown, main branch), sections Public key / Certificate, Sealing key renewal, Key registry init priority order.
Confirmed: `--fetch-cert`, `--cert` file and URL (v0.9.2), `SEALED_SECRETS_CERT`, 30-day renewal since v0.9.x, certificate printed in controller log, private GKE caveat, HSM/KMS note.
Removed: nothing.
Method: documentation only; no commands were run.
