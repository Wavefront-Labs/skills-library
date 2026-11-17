---
id: computing-software.messaging-and-integration.dapr.mtls-self-hosted-mode
name: mtls-self-hosted-mode
category: computing-software
field: messaging-and-integration
product: dapr
tags: [mtls, self-hosted, sentry, trust-anchors, daprd, step-cli, dapr-run]
level: advanced
status: docs-checked
description: "Enable mTLS in self-hosted Dapr: run Sentry with issuer credentials, set DAPR_TRUST_ANCHORS, DAPR_CERT_CHAIN and DAPR_CERT_KEY, enable-mtls flag, step-made certs, rotation."
sources:
  - https://github.com/dapr/docs/blob/v1.15/daprdocs/content/en/operations/security/mtls.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
In self-hosted mode mTLS is off by default. Run Sentry (release binary or built from source), pointing it at a directory for the self-signed root certs:

```bash
./sentry --issuer-credentials <certs-dir> --trust-domain cluster.local
```

Enable it in the Dapr instance configuration:

```yaml
apiVersion: dapr.io/v1alpha1
kind: Configuration
metadata:
  name: daprsystem
  namespace: default
spec:
  mtls:
    enabled: true
```

Each sidecar also needs the certificates through environment variables (Linux/macOS form, with the certs read from your certs directory):

```bash
export DAPR_TRUST_ANCHORS=$(cat <certs-dir>/ca.crt)
export DAPR_CERT_CHAIN=$(cat <certs-dir>/issuer.crt)
export DAPR_CERT_KEY=$(cat <certs-dir>/issuer.key)
export NAMESPACE=default
```

Run with `dapr run --app-id myapp --config ./config.yaml node myapp.js`, or directly:

```bash
daprd --app-id myapp --enable-mtls --sentry-address localhost:50001 --config=./config.yaml
```

Sentry can take a config too (the page shows `workloadCertTTL: "25s"`) via `--config=./config.yaml`.

Bring your own ECDSA PEM certs with the step tool:

```bash
step certificate create cluster.local ca.crt ca.key --profile root-ca --no-password --insecure
step certificate create cluster.local issuer.crt issuer.key --ca ca.crt --ca-key ca.key --profile intermediate-ca --not-after 8760h --no-password --insecure
```

Rotation: delete the generated certs and restart Sentry to regenerate, or copy new `ca.crt`, `issuer.crt`, `issuer.key` to every system service path (default lookup `/var/run/dapr/credentials`) and restart; if the root key changed, restart the Dapr instances.

## Checked

2026-11-08. Read the cited dapr/docs v1.15 page in full and compared each claim; all claims matched the page and none were changed.

Method: documentation only; no commands were run.
